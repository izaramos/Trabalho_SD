# Usando a imagem oficial do Node.js como base
FROM node:14

# Diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copia os arquivos de configuração
COPY node/package.json ./
COPY node/package-lock.json ./

# Instala as dependências do Node.js
RUN npm install

# Copia os arquivos do servidor Node.js
COPY node/index.js ./

# Copia os arquivos de templates (ajustado para a nova localização)
COPY templates ./templates

# Expondo a porta do servidor
EXPOSE 5000

# Comando para iniciar o servidor Node.js
CMD ["node", "index.js"]