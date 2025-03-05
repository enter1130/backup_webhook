import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# 讀取 LINE 設定
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")  # Bot 的 Channel Access Token
LINE_USER_ID = os.getenv("LINE_USER_ID")  # ✅ 這是官方帳號的 `userId`
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # 取得 Webhook JSON 資料
    print("Received Webhook:", data)  # 方便 Debug

    for event in data.get("events", []):
        # ✅ 如果是 `join` 事件（機器人被加入群組）
        if event.get("type") == "join" and event.get("source", {}).get("type") == "group":
            group_id = event["source"]["groupId"]
            print(f"✨ 獲取 `groupId`: {group_id}")

            # ✅ 發送 `groupId` 到官方 LINE 帳號
            send_line_message(LINE_USER_ID, f"🚀 機器人加入了新群組！\n群組 ID: {group_id}")

            return jsonify({"message": f"✨ 獲取群組 ID: {group_id}，已發送至官方帳號"}), 200

    return jsonify({"status": "ok"}), 200


def send_line_message(user_id, message_text):
    """ 發送 LINE 訊息到指定的 `userId`（官方帳號） """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": message_text}]
    }
    response = requests.post(LINE_API_URL, json=payload, headers=headers)
    print(f"📤 發送訊息結果: {response.json()}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
