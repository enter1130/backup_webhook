import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# 讀取 LINE 設定
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
# LINE_USER_ID = os.getenv("LINE_USER_ID")
LINE_GROUP_ID = os.getenv("LINE_GROUP_ID")  # 這裡改成群組 ID
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # 取得 Webhook JSON 資料
    print("Received Webhook:", data)  # 方便 Debug

    # 確保 'message' 欄位存在，否則預設為 '未知通知'
    message_text = data.get("message", "未知通知")

    # 建立 LINE 訊息
    line_message = {
        # "to": LINE_USER_ID,
        "to": LINE_GROUP_ID,
        "messages": [
            {"type": "text", "text": message_text}  # 只傳送 message 內容
        ]
    }

    # 發送 LINE 訊息
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    response = requests.post(LINE_API_URL, json=line_message, headers=headers)

    return jsonify({"status": "ok", "line_response": response.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
