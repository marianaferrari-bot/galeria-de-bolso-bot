# Galeria de Bolso

Bot do Telegram que mostra obras de arte do acervo do Art Institute of Chicago.
Você pode pedir uma obra aleatória ou buscar por artista e tema.

Trabalho do grupo 11 da disciplina Construção de Algoritmos e Programação (UNASP).

**Integrantes:** Mariana Ferrari de Souza e Natanael Felipe

**Bot no Telegram:** @galeriadebolso_bot

## Sobre o projeto

A ideia foi fazer um bot para ver obras de arte direto no Telegram, sem precisar
abrir o site de um museu. Ele recebe o comando, consulta a API do museu e devolve a
imagem da obra com o título, o artista, a data e o link da página dela.

## API utilizada

Art Institute of Chicago API (https://api.artic.edu/docs/). É pública e não precisa
de chave. Usamos o endpoint de busca de obras (`/artworks/search`) e, para exibir
as imagens, o servidor de imagens do próprio museu. Pedimos só obras de domínio
público.

## Comandos

- `/start` e `/ajuda`: mostram os comandos disponíveis
- `/aleatoria`: envia uma obra escolhida ao acaso
- `/arte <termo>`: busca obras por artista, tema ou estilo. Por exemplo: `/arte monet`
- Botão "Outra obra": aparece embaixo de cada imagem e envia outra obra aleatória

Obs.: a busca funciona melhor com palavras em inglês, como `/arte cat`.

## Como rodar

1. Crie um bot com o @BotFather no Telegram (comando `/newbot`) e guarde o token.
2. Baixe o projeto:
   ```
   git clone URL_DO_REPOSITORIO
   cd NOME_DA_PASTA
   ```
3. Instale as bibliotecas:
   ```
   python -m pip install -r requirements.txt
   ```
4. Crie um arquivo chamado `.env` na pasta do projeto, seguindo o modelo do
   `.env.example`, e coloque o seu token:
   ```
   TELEGRAM_TOKEN=seu_token_aqui
   ```
5. Rode o bot:
   ```
   python bot_arte.py
   ```
6. Abra o bot no Telegram e mande `/start`.

O bot só responde enquanto o programa estiver rodando.

## Como o código funciona

O programa fica em um loop que pergunta ao Telegram se chegou mensagem nova
(`getUpdates`). Cada mensagem passa por uma função que identifica o comando e
chama a API do museu. A resposta é enviada de volta com `sendPhoto`. Para não
responder duas vezes à mesma mensagem, guardamos o `update_id` da última
processada. O botão "Outra obra" funciona por meio do `callback_query` do Telegram.

Principais funções do `bot_arte.py`:

- `buscar`, `obra_aleatoria` e `obra_por_termo`: consultam a API do museu
- `formatar` e `url_imagem`: montam o texto e o link da imagem
- `tratar_mensagem`: decide o que fazer com cada comando
- `send`, `send_photo` e `answer_callback`: enviam as respostas pelo Telegram

## Arquivos

- `bot_arte.py`: código do bot
- `requirements.txt`: bibliotecas usadas (`requests` e `python-dotenv`)
- `.env.example`: modelo do arquivo com o token
- `.gitignore`: evita que o `.env` vá para o GitHub

## Divisão do trabalho

- Mariana Ferrari de Souza: integração com a API do museu e comandos do bot
- Natanael Felipe: testes, tratamento de erros, README e repositório

## O que aprendemos

(Escrevam aqui, com as palavras de vocês, o que aprenderam e as dificuldades que
tiveram.)