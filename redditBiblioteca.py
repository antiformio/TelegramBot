import re

import requests


def pedido():
    """ Request """
    response = requests.get(
        "https://www.reddit.com/r/biblioteca/new/.json?limit=50",
        headers={"User-agent": "TelegramBot"},
    )
    jsonResponse = response.json()
    return trataJson(jsonResponse)


def trataJson(obj):
    """ Parse the response """
    resultado = "*Novos posts do /r/bilioteca:*\n\n"
    for post in obj.get("data")["children"]:
        if post["data"]["link_flair_text"] != "Pedido":
            semChars = str(post["data"]["title"]).translate(
                (str.maketrans({"[": "", "]": ""}))
            )
            resultado += "[" + semChars + "]"
            resultado += "(" + post["data"]["url"] + ")" + "\n\n"
    return resultado
