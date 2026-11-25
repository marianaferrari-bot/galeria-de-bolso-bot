import os
import json
import time
import html
import random
import requests
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"

# API do Instituto de Arte de Chicago (sem chave)
API = "https://api.artic.edu/api/v1"
HEADERS = {"AIC-User-Agent": "bot-telegram-aula (projeto da disciplina)"}
CAMPOS = "id,title,artist_display,date_display,image_id"

AJUDA = (
    "🎨 <b>Galeria de Bolso</b>\n"
    "<i>Obras de arte do Art Institute of Chicago, direto no seu Telegram.</i>\n\n"
    "<b>O que eu faço:</b>\n"
    "🎲 /aleatoria - uma obra surpresa\n"
    "🔎 /arte <code>termo</code> - busca por artista, tema ou estilo\n"
    "❓ /ajuda - mostra esta mensagem\n\n"
    "<b>Experimente:</b>\n"
    "/arte monet\n"
    "/arte gato\n"
    "/arte paisagem\n\n"
    "💡 Pode escrever em português, eu traduzo a busca para você!"
)

BOTAO_INICIO = {"inline_keyboard": [[{"text": "🎲 Surpreenda-me", "callback_data": "aleatoria"}]]}
BOTAO_OUTRA = {"inline_keyboard": [[{"text": "🎲 Outra obra", "callback_data": "aleatoria"}]]}

# Dicionário para as buscas mais comuns (o museu só entende inglês)
DICIONARIO = {
    "gato": "cat", "gatos": "cats", "cachorro": "dog", "cão": "dog", "cao": "dog",
    "cavalo": "horse", "pássaro": "bird", "passaro": "bird", "peixe": "fish",
    "leão": "lion", "leao": "lion", "elefante": "elephant", "borboleta": "butterfly",
    "flor": "flower", "flores": "flowers", "árvore": "tree", "arvore": "tree",
    "jardim": "garden", "paisagem": "landscape", "montanha": "mountain",
    "mar": "sea", "rio": "river", "céu": "sky", "ceu": "sky", "sol": "sun",
    "lua": "moon", "noite": "night", "barco": "boat", "navio": "ship",
    "casa": "house", "ponte": "bridge", "cidade": "city", "guerra": "war",
    "mulher": "woman", "homem": "man", "criança": "child", "crianca": "child",
    "retrato": "portrait", "autorretrato": "self-portrait", "anjo": "angel",
    "fruta": "fruit", "frutas": "fruit", "natureza morta": "still life",
    "pintura": "painting", "escultura": "sculpture", "desenho": "drawing",
    "impressionismo": "impressionism", "cubismo": "cubism",
    "surrealismo": "surrealism", "renascimento": "renaissance",
    "barroco": "baroque", "japão": "japan", "japao": "japan",
    "egito": "egypt", "grécia": "greece", "grecia": "greece",
}


# ---------- Telegram ----------
def get_updates(offset):
    r = requests.get(
        f"{BASE}/getUpdates",
        params={"offset": offset, "timeout": 30},
        timeout=40,
    )
    dados = r.json()
    if not dados.get("ok"):  # ex.: 409 = existe outra cópia do bot rodando
        print("Telegram retornou erro:", dados)
        time.sleep(3)
        return []
    return dados.get("result", [])


def send(chat_id, text, html_mode=False, botoes=None):
    data = {"chat_id": chat_id, "text": text}
    if html_mode:
        data["parse_mode"] = "HTML"
    if botoes:
        data["reply_markup"] = json.dumps(botoes)
    requests.post(f"{BASE}/sendMessage", data=data, timeout=10)


def send_photo(chat_id, url, legenda):
    """Envia a foto. Devolve True se deu certo e False se o Telegram recusou."""
    r = requests.post(
        f"{BASE}/sendPhoto",
        data={
            "chat_id": chat_id,
            "photo": url,
            "caption": legenda[:1024],  # limite do Telegram
            "reply_markup": json.dumps(BOTAO_OUTRA),
        },
        timeout=30,
    )
    if not r.ok:
        print("Telegram recusou a foto:", r.status_code, r.text)
    return r.ok


def answer_callback(callback_id):
    requests.post(
        f"{BASE}/answerCallbackQuery",
        data={"callback_query_id": callback_id},
        timeout=10,
    )


# ---------- Tradução (português -> inglês) ----------
def traduzir(termo):
    t = termo.strip().lower()
    if t in DICIONARIO:
        return DICIONARIO[t]
    try:  # se não estiver no dicionário, tenta a API gratuita MyMemory
        r = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": termo, "langpair": "pt|en"},
            timeout=8,
        )
        texto = html.unescape(r.json()["responseData"]["translatedText"]).strip()
        if texto and "MYMEMORY" not in texto.upper():
            return texto
    except Exception as e:
        print("Não consegui traduzir, usando o termo original:", repr(e))
    return termo


# ---------- API externa (Art Institute of Chicago) ----------
def buscar(termo=None, pagina=1, limite=1):
    params = {
        "limit": limite,
        "page": pagina,
        "fields": CAMPOS,
        "query[term][is_public_domain]": "true",  # só obras de domínio público
    }
    if termo:
        params["q"] = termo
    r = requests.get(f"{API}/artworks/search", params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()


def obra_aleatoria():
    # A API recusa páginas muito fundas (erro 403), então sorteamos só entre
    # as primeiras 900 obras: 9 páginas de 100.
    for _ in range(3):
        pagina = random.randint(1, 9)
        try:
            dados = buscar(pagina=pagina, limite=100)["data"]
        except requests.HTTPError as e:
            print("Busca recusada pela API do museu:", e)
            continue
        obras = [o for o in dados if o.get("image_id")]  # algumas não têm imagem
        if obras:
            return random.choice(obras)
    return None


def obra_por_termo(termo):
    obras = buscar(termo=termo, limite=15)["data"]
    obras = [o for o in obras if o.get("image_id")]
    return random.choice(obras) if obras else None


def formatar(obra):
    return (
        f"🖼 {obra['title']}\n"
        f"👤 {obra.get('artist_display') or 'Artista desconhecido'}\n"
        f"📅 {obra.get('date_display') or 's/d'}\n"
        f"🔗 https://www.artic.edu/artworks/{obra['id']}"
    )


def url_imagem(obra):
    return f"https://www.artic.edu/iiif/2/{obra['image_id']}/full/843,/0/default.jpg"


# ---------- Lógica dos comandos ----------
def enviar_obra(chat_id, obra, prefixo=""):
    if obra is None:
        send(chat_id, "Não encontrei nenhuma obra com imagem. Tente outro termo.")
        return
    legenda = (prefixo + "\n\n" if prefixo else "") + formatar(obra)
    if not send_photo(chat_id, url_imagem(obra), legenda):
        send(chat_id, legenda)  # se a foto não carregar, manda pelo menos o texto


def buscar_e_enviar(chat_id, termo):
    termo_en = traduzir(termo)
    obra = obra_por_termo(termo_en)
    if obra is None:
        send(chat_id, f'Não encontrei obras para "{termo}". Tente outro termo.')
        return
    prefixo = f"🔎 Busca: {termo}"
    if termo_en.lower() != termo.lower():
        prefixo += f" → {termo_en}"
    enviar_obra(chat_id, obra, prefixo)


def tratar_mensagem(chat_id, texto):
    partes = texto.strip().split(maxsplit=1)
    comando = partes[0].lower().split("@")[0]  # aceita /arte@nome_do_bot em grupos
    arg = partes[1] if len(partes) > 1 else ""

    if comando in ("/start", "/ajuda"):
        send(chat_id, AJUDA, html_mode=True, botoes=BOTAO_INICIO)
    elif comando == "/aleatoria":
        enviar_obra(chat_id, obra_aleatoria())
    elif comando == "/arte":
        if not arg:
            send(chat_id, "Diga o que você quer ver. Ex.: /arte gato")
        else:
            buscar_e_enviar(chat_id, arg)
    else:
        send(chat_id, "Não conheço esse comando. Use /ajuda para ver as opções.")


# ---------- Loop principal ----------
offset = None
print("Bot de arte rodando... (Ctrl+C para parar)")
while True:
    try:
        updates = get_updates(offset)
    except requests.RequestException as e:
        print("Erro de rede ao falar com o Telegram:", e)
        time.sleep(5)
        continue

    for upd in updates:
        offset = upd["update_id"] + 1
        chat_id = None
        print("Recebido:", "clique no botão" if "callback_query" in upd else "mensagem")
        try:
            msg = upd.get("message")
            if msg and "text" in msg:
                chat_id = msg["chat"]["id"]
                tratar_mensagem(chat_id, msg["text"])

            cb = upd.get("callback_query")  # clique nos botões de "outra obra"
            if cb:
                chat_id = cb["message"]["chat"]["id"]
                answer_callback(cb["id"])
                if cb.get("data") == "aleatoria":
                    enviar_obra(chat_id, obra_aleatoria())
        except Exception as e:
            print("Erro ao tratar a mensagem:", repr(e))
            if chat_id:
                try:
                    send(chat_id, "Ops, não consegui buscar a obra agora. Tente de novo em instantes.")
                except Exception:
                    pass