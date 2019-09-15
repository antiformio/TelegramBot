from flask import Flask, request

from telegramBot import run

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def receive():
    try:
        run(request.json)
        return ""
    except Exception as e:
        print(e)
        return ""


if __name__ == "__main__":
    app.run()
