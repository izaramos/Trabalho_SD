import json
import requests
import schedule
import time
import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = 'ACcc02dc2818833f722b1d72280f9195b6'
TWILIO_AUTH_TOKEN = 'dcf175cc73ecf75ce25472f50161674f'
TWILIO_PHONE_NUMBER = '+19387585682'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def enviar_alertas():
    try:
        response = requests.get('http://localhost:5000/cotacao_euro')
        if response.status_code == 200:
            cotacao_data = response.json()
            valorEuro = float(cotacao_data.get('valor', 0))
            print(f"Valor do euro obtido: R${valorEuro}")
        else:
            valorEuro = 0
            print(f"Falha ao obter cotação do euro, status code: {response.status_code}")

        if os.path.exists('alertas.json'):
            with open('alertas.json', 'r') as file:
                alertas = json.load(file)
        else:
            alertas = []
            print("Arquivo alertas.json não encontrado.")

        novos_alertas = []

        for alerta in alertas:
            if alerta['valorMenor'] < valorEuro:
                if alerta['tipo'] == 'sms':
                    message = client.messages.create(
                        body=f'A cotação do euro está abaixo de R${alerta["valorMenor"]}!',
                        from_=TWILIO_PHONE_NUMBER,
                        to=alerta['telefone']
                    )
                    print(f"SMS enviado para {alerta['telefone']}, SID: {message.sid}")
            else:
                novos_alertas.append(alerta)

        # Atualizar o arquivo alertas.json
        with open('alertas.json', 'w') as file:
            json.dump(novos_alertas, file, indent=4)
            print("Arquivo alertas.json atualizado com sucesso.")

    except Exception as e:
        print(f"Erro ao enviar alertas: {str(e)}")

# Agendar a execução da função todos os dias às 10:05
schedule.every().day.at("10:05").do(enviar_alertas)

print("Iniciando o loop de agendamento.")

# Loop para manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(60)  # Espera um minuto para checar a próxima tarefa