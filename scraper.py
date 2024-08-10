import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request
from datetime import datetime
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client

app = Flask(__name__)
scheduler = BackgroundScheduler()

TWILIO_ACCOUNT_SID = 'ACcc02dc2818833f722b1d72280f9195b6'
TWILIO_AUTH_TOKEN = 'dcf175cc73ecf75ce25472f50161674f'
TWILIO_PHONE_NUMBER = '+19387585682'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_euro_cotation():
    URL = "https://br.investing.com/currencies/eur-brl"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        valorEuro = soup.find("div", class_="text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]")
        
        if valorEuro:
            cotacao = valorEuro.text.strip().replace(',', '.')
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            return {'data': timestamp.split()[0], 'valor': cotacao}
        else:
            return {'data': datetime.now().strftime("%d/%m/%Y"), 'valor': None}
    
    except Exception as e:
        print(f"Erro ao obter cotação do euro: {e}")
        return {'data': datetime.now().strftime("%d/%m/%Y"), 'valor': None}

def save_cotation_to_json(data):
    filename = 'cotacoes.json'
    if os.path.exists(filename):
        with open(filename, 'r+') as file:
            cotacoes = json.load(file)
            cotacoes.append(data)
            file.seek(0)
            json.dump(cotacoes, file, indent=4)
    else:
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)

def fetch_and_save_cotation():
    data = get_euro_cotation()
    save_cotation_to_json(data)

# Agenda a captura de cotação diariamente às 10:00
scheduler.add_job(fetch_and_save_cotation, 'cron', hour=10, minute=0)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/cotacao_euro')
def cotacao_euro():
    data = get_euro_cotation()
    save_cotation_to_json(data)
    return jsonify(data)

@app.route('/historico_cotacoes')
def historico_cotacoes():
    filename = 'cotacoes.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            cotacoes = json.load(file)
        return jsonify(cotacoes)
    else:
        return jsonify([])

def get_historico_cotacoes():
    if not os.path.exists('cotacoes.json'):
        return []
    with open('cotacoes.json', 'r') as f:
        data = json.load(f)
    return data

@app.route('/get_alertas', methods=['GET'])
def get_alertas():
    try:
        with open('alertas.json', 'r') as file:
            alertas = json.load(file)
        return jsonify(alertas)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/notify_sms', methods=['POST'])
def notify_sms():
    data = request.get_json()
    phone = data.get('phone')
    valorInformado = data.get('valorInformado')

    if not phone or valorInformado is None:
        return jsonify({'status': 'error', 'message': 'Telefone e valor informado são obrigatórios!'}), 400

    # Adicionando o código do país automaticamente
    if not phone.startswith('+'):
        phone = '+55' + phone

    try:
        with open('alertas.json', 'r') as file:
            alertas = json.load(file)

        novo_alerta = {
            "tipo": "sms",
            "valorMenor": float(valorInformado),
            "telefone": phone
        }
        alertas.append(novo_alerta)

        with open('alertas.json', 'w') as file:
            json.dump(alertas, file, indent=4)

        return jsonify({'status': 'success', 'message': 'Alerta adicionado com sucesso!'})

    except Exception as e:
        print("Erro ao processar solicitação:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# http://localhost:5000/ --> Tela com os dados