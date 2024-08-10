# Dockerfile
# Usar a imagem oficial do Ubuntu
FROM ubuntu:latest

# Atualizar pacotes e instalar dependências
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nano

# Criar um diretório de trabalho
WORKDIR /app

# Criar e ativar um ambiente virtual
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade pip

# Instalar BeautifulSoup e outras bibliotecas Python necessárias no ambiente virtual
COPY requirements.txt .
RUN /venv/bin/pip install -r requirements.txt

# Copiar todos os arquivos do diretório atual para o contêiner
COPY . /app

# Configurar o PATH para usar o ambiente virtual
ENV PATH="/venv/bin:$PATH"

# Comando para rodar o container
CMD ["python3", "scraper.py"]