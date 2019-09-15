import datetime
import io

import requests

semana = {
    0: "Segunda-Feira",
    1: "Terça-Feira",
    2: "Quarta-Feira",
    3: "Quinta-Feira",
    4: "Sexta-Feira",
    5: "Sábado",
    6: "Domingo",
}


def pedidoEsp():
    response = requests.get(
        "https://www.el-tiempo.net/api/json/v1/provincias/08/municipios/08019/weather"
    )
    jsonResponse = response.json()
    return trataJson(jsonResponse)


def trataJson(obj):
    texto = ""
    tudo = obj.get("prediccion")
    dias = tudo.get("dia")

    for dia in range(0, len(dias) - 3):
        texto += str(
            semana.get(
                datetime.datetime.weekday(
                    datetime.datetime.strptime(
                        dias[dia].get("@attributes").get("fecha"), "%Y-%m-%d"
                    )
                )
            )
            + "\n"
        )
        data = dias[dia].get("@attributes").get("fecha")
        tempMaxima = dias[dia].get("temperatura").get("maxima")
        tempMinima = dias[dia].get("temperatura").get("minima")
        sensTermicaMaxima = dias[dia].get("sens_termica").get("maxima")
        sensTermicaMinima = dias[dia].get("sens_termica").get("minima")
        texto += f"Dia: {data} \nMáxima: {tempMaxima} FeelsLike: {sensTermicaMaxima}\nMinima: {tempMinima} FeelsLike: {sensTermicaMinima}\n"
        probRain = dias[dia].get("prob_precipitacion")
        if dia > 0:
            if type(probRain) == list:
                texto += f"Probabilidade de Chuva: {probRain[0]}%\n\n"
            else:
                texto += f"Probabilidade de Chuva: {probRain}%\n\n"
        else:
            texto += "\n"
    return texto
