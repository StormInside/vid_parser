from flask import Flask, request
import requests

app = Flask(__name__)
@app.route("/message")
def serve():
    data = request.args.get('text')
    send_message(data)
    return {"ok": True}

API_TOKEN = '1395702772:AAG3LI7mtJHfZCzvrChL_I7YAdbaB4J7fg8'
chat_id = 556487045

def send_message(text):
    method = "sendMessage"
    token = API_TOKEN
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)