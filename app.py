import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# 讀取 LINE 設定
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # 取得 Webhook JSON 資料
    print("Received Webhook:", data)  # 方便 Debug

    # 確保事件存在
    if "events" in data:
        for event in data["events"]:
            # 如果是群組邀請事件 (join)
            if event["type"] == "join" and event["source"]["type"] == "group":
                group_id = event["source"]["groupId"]
                message_text = f"機器人已加入群組，Group ID: {group_id}"  # 記錄 Group ID

                # 發送 Group ID 到你的個人 LINE
                line_message = {
                    "to": LINE_USER_ID,
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

                return jsonify({"status": "ok", "group_id": group_id, "line_response": response.json()})

    return jsonify({"status": "no_valid_event"})  # 若沒有有效事件，回傳預設 JSON
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
