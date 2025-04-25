# Capturador de Localização

Uma aplicação web simples que captura e salva a geolocalização dos visitantes.

## Requisitos

- Node.js (versão 14 ou superior)
- NPM (gerenciador de pacotes do Node.js)

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
npm install
```

## Como usar

1. Inicie o servidor:
```bash
npm start
```

2. Abra seu navegador e acesse:
```
http://localhost:3000
```

3. Clique no botão "Compartilhar Localização" e permita o acesso à sua localização quando solicitado pelo navegador.

## Funcionalidades

- Interface web amigável
- Captura de latitude e longitude
- Armazenamento em banco de dados SQLite
- Registro de timestamp para cada localização

## Visualizando os dados

Para ver todas as localizações salvas, acesse:
```
http://localhost:3000/localizacoes
```

## Observações

- Esta aplicação requer permissão do usuário para acessar a localização
- Os dados são armazenados localmente em um arquivo SQLite
- A aplicação funciona apenas em navegadores que suportam a API de Geolocalização 