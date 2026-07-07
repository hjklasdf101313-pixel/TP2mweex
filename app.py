
from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Sinyal masuk:", data)
    return "ok", 200

@app.route("/")
def home():
    return "Bot Jalan", 200
