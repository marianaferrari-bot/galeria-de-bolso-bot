# 🎨 Galeria de Bolso

Bot de Telegram que mostra obras de arte do acervo do **Instituto de Arte de Chicago**.
Procure o bot no Telegram: **@galeriadebolso_bot**

- **API externa:** [Art Institute of Chicago API](https://api.artic.edu/docs/) (pública, sem chave)
- **Disciplina:** Construir Algoritmos - UNASP
- **Grupo:** 11
- **Integrantes:** Mariana Ferrari de Souza, Natanael Felipe

## Comandos

| Comando | O que faz |
|---|---|
| `/start` ou `/ajuda` | Mostra a lista de comandos |
| `/aleatoria` | Envia uma obra surpresa (domínio público) |
| `/arte <termo>` | Busca por tema, artista ou estilo (ex.: `/arte monet`) |
| Botão **🎲 Outra obra** | Aparece abaixo de cada imagem e envia outra obra aleatória |

Cada resposta traz imagem, título, artista, data e link da obra no site do museu.
A busca funciona melhor com termos em inglês (ex.: `/arte cat`).

## Como executar

1. Crie um bot no Telegram com o `@BotFather` (`/newbot`) e copie o token.
2. Clone o repositório e entre na pasta:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_REPOSITORIO>
   ```
3. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como modelo):
   ```
   TELEGRAM_TOKEN=seu_token_aqui
   ```
5. Rode o bot:
   ```bash
   python bot_arte.py
   ```
6. Abra o bot no Telegram e envie `/start`.

O bot só responde enquanto o programa estiver rodando.

## Como funciona

O bot usa *long polling*: consulta o método `getUpdates` da API do Telegram,
trata cada mensagem e responde com `sendMessage` ou `sendPhoto`.
As obras vêm do endpoint `/artworks/search` da API do museu, e as imagens são
servidas pelo servidor de imagens (IIIF) do próprio museu. O botão
"Outra obra" usa `callback_query` do Telegram.

## Estrutura do projeto

```
├── bot_arte.py        # código do bot
├── requirements.txt   # dependências
├── .env.example       # modelo do arquivo de configuração
├── .gitignore         # evita enviar o .env ao GitHub
└── README.md
```

## Divisão do trabalho

- Nome 1: integração com a API do museu
- Nome 2: comandos e interação com o Telegram
- Nome 3: testes e tratamento de erros
- Nome 4: README, repositório e apresentação