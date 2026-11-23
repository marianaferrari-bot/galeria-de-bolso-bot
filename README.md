<h1 align="center">🖼️ Galeria de Bolso</h1>

<p align="center">
  Um bot do Telegram que leva obras de arte do Art Institute of Chicago direto para a sua conversa.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/API-Art%20Institute%20of%20Chicago-B22222" alt="API">
</p>

<p align="center">
  Trabalho do <b>Grupo 11</b> · Construção de Algoritmos e Programação · UNASP<br>
  <b>Mariana Ferrari de Souza</b> e <b>Natanael Felipe</b><br>
  Bot no Telegram: <b>@galeriadebolso_bot</b>
</p>

---

## 📖 Sobre o projeto

A ideia foi poder ver obras de arte direto no Telegram, sem precisar abrir o site de um
museu. O bot recebe um comando, consulta a API do museu e devolve a imagem da obra com
título, artista, data e o link da página dela.

## ✨ Funcionalidades

| Comando | O que faz |
|---|---|
| `/start` e `/ajuda` | Mostram os comandos disponíveis |
| `/aleatoria` | Envia uma obra escolhida ao acaso |
| `/arte <termo>` | Busca obras por artista, tema ou estilo (ex.: `/arte monet`) |
| Botão **Outra obra** | Aparece embaixo de cada imagem e envia outra obra aleatória |

> A busca funciona melhor com palavras em inglês, como `/arte cat`.

## 🔌 API utilizada

**[Art Institute of Chicago API](https://api.artic.edu/docs/)**: pública e sem necessidade
de chave. Usamos o endpoint de busca de obras (`/artworks/search`) e o servidor de imagens
do próprio museu. Pedimos apenas obras de domínio público.

## 🚀 Como rodar

1. Crie um bot com o **@BotFather** no Telegram (comando `/newbot`) e guarde o token.
2. Baixe o projeto:
   ```
   git clone URL_DO_REPOSITORIO
   cd NOME_DA_PASTA
   ```
3. Instale as bibliotecas:
   ```
   python -m pip install -r requirements.txt
   ```
4. Crie um arquivo chamado `.env` na pasta do projeto (use o `.env.example` como modelo)
   e coloque o seu token:
   ```
   TELEGRAM_TOKEN=seu_token_aqui
   ```
5. Rode o bot:
   ```
   python bot_arte.py
   ```
6. Abra o bot no Telegram e envie `/start`.

> O bot só responde enquanto o programa estiver rodando.

## ⚙️ Como o código funciona

O programa fica em um loop perguntando ao Telegram se chegou mensagem nova (`getUpdates`).
Cada mensagem passa por uma função que identifica o comando e chama a API do museu. A
resposta volta para o usuário com `sendPhoto`. Para não responder duas vezes à mesma
mensagem, guardamos o `update_id` da última processada. O botão "Outra obra" funciona
por meio do `callback_query` do Telegram.

Principais funções do `bot_arte.py`:

- `buscar`, `obra_aleatoria` e `obra_por_termo`: consultam a API do museu
- `formatar` e `url_imagem`: montam o texto e o link da imagem
- `tratar_mensagem`: decide o que fazer com cada comando
- `send`, `send_photo` e `answer_callback`: enviam as respostas pelo Telegram

## 📁 Estrutura do projeto

```
├── bot_arte.py        código do bot
├── requirements.txt   bibliotecas usadas (requests e python-dotenv)
├── .env.example       modelo do arquivo com o token
├── .gitignore         evita que o .env vá para o GitHub
└── README.md
```

## 👥 Divisão do trabalho

- **Mariana Ferrari de Souza:** integração com a API do museu e comandos do bot
- **Natanael Felipe:** testes, tratamento de erros, README e repositório

## 💡 O que aprendemos

- Como um bot do Telegram funciona por trás: token, `getUpdates` e envio de mensagens.
- Como consumir uma API externa com `requests` e aproveitar só os campos do JSON que importam.
- Como proteger o token usando `.env` e `.gitignore`.
- Como tratar problemas reais, como obras sem imagem e erros de rede.
- Como usar Git e GitHub para guardar e entregar o projeto.