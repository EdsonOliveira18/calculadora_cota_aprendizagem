<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Ponto</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .button {
            padding: 10px 20px;
            margin: 10px;
            cursor: pointer;
            border: none;
            background-color: #4CAF50;
            color: white;
        }
        input {
            padding: 10px;
            margin: 10px;
            width: 200px;
        }
    </style>
</head>
<body>
    <h1>Sistema de Ponto</h1>
    <input type="text" id="cpf" placeholder="Digite seu CPF" />
    <button class="button" onclick="register('entrada')">Registrar Entrada</button>
    <button class="button" onclick="register('saida')">Registrar Saída</button>
    <h2>Registros de Ponto</h2>
    <ul id="records"></ul>

    <script src="app.js"></script>
</body>
</html>

async function register(type) {
    const cpf = document.getElementById('cpf').value;
    if (!validateCPF(cpf)) {
        alert('CPF inválido');
        return;
    }
    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cpf, type })
    });
    const result = await response.json();
    if (result.success) {
        alert('Registro de ' + type + ' feito com sucesso!');
        loadRecords();
    } else {
        alert('Falha ao registrar ' + type);
    }
}

async function loadRecords() {
    const response = await fetch('/records');
    const records = await response.json();
    const recordsList = document.getElementById('records');
    recordsList.innerHTML = '';
    records.forEach(record => {
        const listItem = document.createElement('li');
        listItem.textContent = `${record.cpf} - ${record.type} - ${new Date(record.timestamp).toLocaleString()}`;
        recordsList.appendChild(listItem);
    });
}

function validateCPF(cpf) {
    // Função básica para validar CPF
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11) return false;
    let sum = 0;
    let rest;
    if (cpf === "00000000000") return false;
    for (let i = 1; i <= 9; i++) sum = sum + parseInt(cpf.substring(i-1, i)) * (11 - i);
    rest = (sum * 10) % 11;
    if ((rest === 10) || (rest === 11)) rest = 0;
    if (rest !== parseInt(cpf.substring(9, 10))) return false;
    sum = 0;
    for (let i = 1; i <= 10; i++) sum = sum + parseInt(cpf.substring(i-1, i)) * (12 - i);
    rest = (sum * 10) % 11;
    if ((rest === 10) || (rest === 11)) rest = 0;
    if (rest !== parseInt(cpf.substring(10, 11))) return false;
    return true;
}

document.addEventListener('DOMContentLoaded', loadRecords);


const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

let records = [];

app.use(bodyParser.json());
app.use(express.static('public'));

app.post('/register', (req, res) => {
    const { cpf, type } = req.body;
    if (validateCPF(cpf) && (type === 'entrada' || type === 'saida')) {
        const timestamp = new Date();
        records.push({ cpf, type, timestamp });
        res.json({ success: true });
    } else {
        res.json({ success: false });
    }
});

app.get('/records', (req, res) => {
    res.json(records);
});

function validateCPF(cpf) {
    // Função básica para validar CPF
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11) return false;
    let sum = 0;
    let rest;
    if (cpf === "00000000000") return false;
    for (let i = 1; i <= 9; i++) sum = sum + parseInt(cpf.substring(i-1, i)) * (11 - i);
    rest = (sum * 10) % 11;
    if ((rest === 10) || (rest === 11)) rest = 0;
    if (rest !== parseInt(cpf.substring(9, 10))) return false;
    sum = 0;
    for (let i = 1; i <= 10; i++) sum = sum + parseInt(cpf.substring(i-1, i)) * (12 - i);
    rest = (sum * 10) % 11;
    if ((rest === 10) || (rest === 11)) rest = 0;
    if (rest !== parseInt(cpf.substring(10, 11))) return false;
    return true;
}

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
