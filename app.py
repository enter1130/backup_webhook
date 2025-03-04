import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# 從 Render 環境變數讀取 LINE Bot API 設定
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")  # 在 Render 設定
LINE_USER_ID = os.getenv("LINE_USER_ID")  # 你的 LINE User ID
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # 取得 Webhook 傳來的 JSON 資料
    print("Received Webhook:", data)  # 紀錄輸入，方便 Debug

    # 建立 LINE Bot 訊息
    line_message = {
        "to": LINE_USER_ID,
        "messages": [
            {"type": "text", "text": f"收到 Webhook 通知：\n{data}"}
        ]
    }

    # 發送訊息到 LINE
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    response = requests.post(LINE_API_URL, json=line_message, headers=headers)

    # 回傳 Webhook 結果
    return jsonify({"status": "ok", "line_response": response.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
