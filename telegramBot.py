import json

import config
import futebol
import redditBiblioteca
import requests
import tempo
import ligaRecord

# The main URL for the Telegram API with our bot's token
BASE_URL = "https://api.telegram.org/bot{}".format(config.bot_token)


def receive_message(message):
    """Receive a raw message from Telegram"""
    try:
        resultado = message["message"]["text"]
        chat_id = message["message"]["chat"]["id"]
        return resultado, chat_id
    except Exception as e:
        print(e)
        return (None, None)


def handle_message(message, chat_id):
    """Calculate a response to the message"""
    if "/tempo" in message:
        message = tempo.pedidoEsp()
    elif "/livros" in message:
        message = redditBiblioteca.pedido()
    elif "/bolahoje" in message:
        data = futebol.request()
        message = futebol.jogosHoje(data)
    elif "/bolasemana" in message:
        data = futebol.request()
        message = futebol.jogosSemana(data)
    elif "/liga" in message:
        message = ligaRecord.reduceTableDetails(ligaRecord.getTabela())
    elif "/help" in message:
        message = (
            "*Comandos:*\n\n"
            "*/tempo* - Retorna o tempo em Barcelona por 5 dias.\n"
            "*/livros* - Lista de livros novos no /r/biblioteca\n"
            "*/bolahoje* - Jogos de Hoje\n"
            "*/bolasemana* - Jogos da semana\n"
        )
        send_keyboard(chat_id)
    else:
        message = "Comando desconhecido...\n\nEscreva */help* para obter a lista de comandos!\n"
    return message


def send_photo(chat_id, urlPhoto):
    data = {"chat_id": chat_id, "photo": urlPhoto}
    url = BASE_URL + "/sendPhoto"
    try:
        response = requests.post(url, data).content
    except Exception as e:
        print(e)


def send_message(message, chat_id):
    """Send a message to the Telegram chat defined by chat_id"""
    data = {
        "text": message.encode("utf8"),
        "chat_id": chat_id,
        "parse_mode": "Markdown",
    }
    url = BASE_URL + "/sendMessage"
    try:
        response = requests.post(url, data).content
    except Exception as e:
        print(e)


def send_keyboard(chat_id):
    """Send the keyboard to the Telegram chat defined by chat_id"""
    text = "Opções"
    reply_markup = {"keyboard": [["/bolasemana", "/bolahoje"], ["/tempo"], ["/livros"], ["/liga"]]}
    data = {"chat_id": chat_id, "text": text, "reply_markup": json.dumps(reply_markup)}
    url = BASE_URL + "/sendMessage"
    try:
        response = requests.post(url, data).content
    except Exception as e:
        print(e)


def run(message):
    """Receive a message, handle it, and send a response"""
    # send_photo(chat_id, 'https://www.schmengler-se.de/wp-content/uploads/2016/09/helper.png')
    try:
        message, chat_id = receive_message(message)
        response = handle_message(message, chat_id)
        send_message(response, chat_id)
    except Exception as e:
        print(e)
