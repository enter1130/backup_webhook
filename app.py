import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# 讀取 LINE 設定
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

# 全局變數存儲最新的 userId
latest_user_id = None

@app.route("/webhook", methods=["POST"])
def webhook():
    global latest_user_id  # 允許修改全局變數
    data = request.json  # 取得 Webhook JSON 資料
    print("Received Webhook:", data)  # 方便 Debug

    for event in data.get("events", []):
        # ✅ 如果是 `follow` 事件（使用者加好友）
        if event.get("type") == "follow" and event.get("source", {}).get("type") == "user":
            latest_user_id = event["source"]["userId"]
            print(f"✨ 獲取 `userId`: {latest_user_id}")
            return jsonify({"message": f"✨ 獲取使用者 ID: {latest_user_id}"}), 200

    # 如果是一般訊息推送，確保 `latest_user_id` 已經獲取
    if latest_user_id is None:
        return jsonify({"error": "❌ 無法發送，因為尚未獲取 `userId`"}), 400

    # 取得要發送的訊息
    message_text = data.get("message", "未知通知")

    # 建立 LINE 訊息
    line_message = {
        "to": latest_user_id,
        "messages": [
            {"type": "text", "text": message_text}
        ]
    }

    # 發送 LINE 訊息
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    response = requests.post(LINE_API_URL, json=line_message, headers=headers)

    return jsonify({"status": "ok", "userId": latest_user_id, "line_response": response.json()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
