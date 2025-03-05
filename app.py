import os

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request

app = Flask(__name__)

# 讀取 Render 網址
RENDER_URL = os.getenv("RENDER_URL", "https://你的-render-網址")

# 定期 Ping 自己的函數
def keep_alive():
    try:
        print("🔄 保持活動狀態：發送 /ping")
        requests.get(f"{RENDER_URL}/ping")
    except Exception as e:
        print(f"⚠️ 無法發送 Keep Alive 請求: {e}")

# 建立 APScheduler 排程器
scheduler = BackgroundScheduler()
scheduler.add_job(keep_alive, "interval", minutes=10)
scheduler.start()

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

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
