# Usando a imagem oficial do Node.js como base
FROM node:18

# Diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copia os arquivos de configuração
COPY node/package.json ./
COPY node/package-lock.json ./

# Instala as dependências do Node.js
RUN npm install

# Copia os arquivos do servidor Node.js
COPY node/index.js ./
COPY node/templates ./templates

# Copia os arquivos de dados e scripts do Python
COPY data ./data
COPY python/scheduler.py ./
COPY python/scraper.py ./

# Ajusta as permissões dos arquivos copiados
RUN chmod -R 755 /usr/src/app

# Expondo a porta do servidor
EXPOSE 5000

# Comando para iniciar o servidor Node.js
CMD ["node", "index.js"]