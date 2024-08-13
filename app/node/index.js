const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const axios = require('axios');
const app = express();
const port = 5000;

app.use(cors());

// Configuração para servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'templates')));

// Configuração para servir arquivos da pasta data
app.use('/data', express.static(path.join(__dirname, 'data')));

// Middleware para parsear o corpo das requisições como JSON
app.use(express.json());

// Rota para obter histórico de cotações
app.get('/historico_cotacoes', (req, res) => {
    const filePath = path.join(__dirname, 'data', 'cotacoes.json');
    console.log(`Lendo arquivo de histórico de cotações: ${filePath}`);
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Erro ao ler o arquivo cotacoes.json:', err);
            return res.status(500).json({ error: 'Erro interno do servidor' });
        }
        try {
            const parsedData = JSON.parse(data);
            res.json(parsedData);
        } catch (parseError) {
            console.error('Erro ao parsear o arquivo cotacoes.json:', parseError);
            res.status(500).json({ error: 'Erro interno do servidor' });
        }
    });
});

// Rota para obter a cotação atual do euro
app.get('/cotacao_euro', (req, res) => {
    const filePath = path.join(__dirname, 'data', 'cotacoes.json');
    console.log(`Lendo arquivo de cotações para obter a cotação atual: ${filePath}`);
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Erro ao ler o arquivo cotacoes.json:', err);
            return res.status(500).json({ error: 'Erro interno do servidor' });
        }
        try {
            const cotacoes = JSON.parse(data);
            // Supondo que você tenha uma estrutura onde o último item é a cotação mais recente
            const cotacaoAtual = cotacoes[cotacoes.length - 1];
            res.json(cotacaoAtual);
        } catch (parseError) {
            console.error('Erro ao parsear o arquivo cotacoes.json:', parseError);
            res.status(500).json({ error: 'Erro interno do servidor' });
        }
    });
});

const alertasFilePath = path.join(__dirname, 'alertas.json');
// Função para inicializar o arquivo de alertas se não existir
function initializeAlertasFile() {
    if (!fs.existsSync(alertasFilePath)) {
        console.log('Criando arquivo de alertas...');
        fs.writeFileSync(alertasFilePath, JSON.stringify([], null, 4));
    }
}
// Chama a função ao iniciar o servidor
initializeAlertasFile();

// Rota para notificar via SMS
app.post('/notify_sms', (req, res) => {
    const { phone, valorInformado } = req.body;
    const filePath = path.join(__dirname, 'data', 'cotacoes.json');

    console.log(`Lendo arquivo de cotações para verificar a cotação atual: ${filePath}`);
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Erro ao ler o arquivo cotacoes.json:', err);
            return res.status(500).json({ error: 'Erro interno do servidor' });
        }

        try {
            const cotacoes = JSON.parse(data);
            const cotacaoAtual = cotacoes[cotacoes.length - 1];

            if (valorInformado < parseFloat(cotacaoAtual.valor.replace(',', '.'))) {
                initializeAlertasFile();  // Garantir que o arquivo exista
                fs.readFile(alertasFilePath, 'utf8', (err, alertasData) => {
                    if (err) {
                        console.error('Erro ao ler o arquivo alertas.json:', err);
                        return res.status(500).json({ error: 'Erro interno do servidor' });
                    }
                    const alertas = JSON.parse(alertasData);
                    const novo_alerta = {
                        tipo: 'sms',
                        valorMenor: valorInformado,
                        telefone: phone
                    };
                    alertas.push(novo_alerta);

                    fs.writeFile(alertasFilePath, JSON.stringify(alertas, null, 4), 'utf8', (err) => {
                        if (err) {
                            console.error('Erro ao escrever no arquivo alertas.json:', err);
                            return res.status(500).json({ error: 'Erro interno do servidor' });
                        }
                        res.json({ status: 'success', message: 'Alerta enviado com sucesso!' });
                    });
                });
            } else {
                res.json({ status: 'error', message: 'A cotação atual está acima do valor informado.' });
            }
        } catch (parseError) {
            console.error('Erro ao parsear o arquivo cotacoes.json:', parseError);
            res.status(500).json({ error: 'Erro interno do servidor' });
        }
    });
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'frontend.html'));
    axios.get('http://python_server:5001/start_scraper')
    .then(response => console.log('Scraper inicializado:', response.data))
    .catch(error => console.error('Erro ao inicializar o scraper:', error));
});

app.listen(port, () => {
    console.log(`Servidor Node.js rodando na porta ${port}`);
});
