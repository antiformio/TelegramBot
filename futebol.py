import re
from datetime import datetime

import bs4
import requests


def request():
    """ Request and partial edit of the response """
    res = requests.get("https://ondebola.com/")
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    tables = soup.findChildren("table")
    listaJogos = tables[0]

    jogos = listaJogos.findChildren(["tr"])
    jogos = jogos[1 : len(jogos) - 1]

    return jogos


def getSpainTime(date):
    hora_espanha = datetime.strptime(date[-6:].strip(), "%H:%M")
    horas = hora_espanha.hour + 1
    minutos = hora_espanha.minute
    return horas, minutos


def jogosHoje(jogos):
    """ Games of the day """
    mensagem = ""
    pedidos = re.compile(r"(?:hoje|Hoje)", re.IGNORECASE)
    for jogo in jogos:
        celulas = jogo.findChildren("td")
        if pedidos.findall(celulas[0].text):
            data = celulas[0].text.strip("hoje")
            horas, minutos = getSpainTime(data)
            equipas = jogo.findAll("span", {"class": "team"})
            casa = equipas[0].text
            fora = equipas[1].text
            canal = celulas[2].contents[1].text.strip(" \r\n\t")
            mensagem += (
                str(horas)
                + ":"
                + str(minutos)
                + " *"
                + casa
                + "*"
                + " vs "
                + "*"
                + fora
                + "*"
                + " "
                + canal
                + "\n\n"
            )
        else:
            continue
    return mensagem


def jogosSemana(jogos):
    """ Games of the week """
    mensagem = ""
    for jogo in jogos:
        celulas = jogo.findChildren("td")
        data = celulas[0].text.strip("hoje")
        horas, minutos = getSpainTime(data)
        equipas = jogo.findAll("span", {"class": "team"})
        casa = equipas[0].text
        fora = equipas[1].text
        canal = celulas[2].contents[1].text.strip(" \r\n\t")
        mensagem += (
            data[:10]
            + " "
            + str(horas)
            + ":"
            + str(minutos)
            + " "
            + "*"
            + casa
            + "*"
            + " vs "
            + "*"
            + fora
            + "*"
            + " "
            + canal
            + "\n\n"
        )
    return mensagem
