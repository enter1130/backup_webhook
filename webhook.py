import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# 載入 .env 檔案
load_dotenv()

app = Flask(__name__)

# 讀取環境變數
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # 接收 Webhook 資料
    print("Received Webhook:", data)

    # 發送 LINE 訊息
    line_message = {
        "to": LINE_USER_ID,
        "messages": [
            {"type": "text", "text": f"Webhook 通知：{data}"}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    response = requests.post(LINE_API_URL, json=line_message, headers=headers)

    return jsonify({"status": "ok", "line_response": response.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
