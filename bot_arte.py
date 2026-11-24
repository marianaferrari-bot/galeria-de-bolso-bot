import os
import json
import time
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
    "🎨 Bot de Arte - acervo do Instituto de Arte de Chicago\n\n"
    "/aleatoria - uma obra surpresa\n"
    "/arte <termo> - busca por tema, artista ou estilo\n"
    "   ex.: /arte monet, /arte gato, /arte impressionismo\n"
    "/ajuda - mostra esta mensagem"
)


# ---------- Telegram ----------
def get_updates(offset):
    r = requests.get(
        f"{BASE}/getUpdates",
        params={"offset": offset, "timeout": 30},
        timeout=40,
    )
    return r.json().get("result", [])


def send(chat_id, text):
    requests.post(
        f"{BASE}/sendMessage",
        data={"chat_id": chat_id, "text": text},
        timeout=10,
    )


def send_photo(chat_id, url, legenda):
    """Envia a foto. Devolve True se deu certo e False se o Telegram recusou."""
    botao = {"inline_keyboard": [[{"text": "🎲 Outra obra", "callback_data": "aleatoria"}]]}
    r = requests.post(
        f"{BASE}/sendPhoto",
        data={
            "chat_id": chat_id,
            "photo": url,
            "caption": legenda[:1024],  # limite do Telegram
            "reply_markup": json.dumps(botao),
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
    total = buscar()["pagination"]["total"]
    for _ in range(5):  # algumas obras não têm imagem, então tenta de novo
        pagina = random.randint(1, min(total, 5000))
        dados = buscar(pagina=pagina)["data"]
        if dados and dados[0].get("image_id"):
            return dados[0]
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
def enviar_obra(chat_id, obra):
    if obra is None:
        send(chat_id, "Não encontrei nenhuma obra com imagem. Tente outro termo.")
        return
    ok = send_photo(chat_id, url_imagem(obra), formatar(obra))
    if not ok:  # se a foto não carregar, manda pelo menos o texto com o link
        send(chat_id, formatar(obra))


def tratar_mensagem(chat_id, texto):
    partes = texto.strip().split(maxsplit=1)
    comando = partes[0].lower()
    arg = partes[1] if len(partes) > 1 else ""

    if comando in ("/start", "/ajuda"):
        send(chat_id, AJUDA)
    elif comando == "/aleatoria":
        enviar_obra(chat_id, obra_aleatoria())
    elif comando == "/arte":
        if not arg:
            send(chat_id, "Informe um termo. Ex.: /arte monet")
        else:
            enviar_obra(chat_id, obra_por_termo(arg))
    else:
        send(chat_id, "Comando não reconhecido. Use /ajuda.")


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
        try:
            msg = upd.get("message")
            if msg and "text" in msg:
                chat_id = msg["chat"]["id"]
                tratar_mensagem(chat_id, msg["text"])

            cb = upd.get("callback_query")  # clique no botão "Outra obra"
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