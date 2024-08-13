# Usando a imagem base do Python
FROM python:3.10

# Definir o diretório de trabalho
WORKDIR /usr/src/app

# Copiar os arquivos de requisitos e instalar dependências
COPY python/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos
COPY python/ ./
COPY data ./data

# Expor a porta em que o app vai rodar
EXPOSE 5001

# Comando para iniciar o aplicativo
CMD ["python", "scraper.py"]