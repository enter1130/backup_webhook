# 使用 Python 3.9
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製程式碼到容器
COPY app.py .
COPY requirements.txt .
# COPY .env .  # 加入環境變數設定檔（避免寫死在程式碼中）

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 確保 Webhook 在 NAS 上可存取
EXPOSE 5000

# 使用 Gunicorn 啟動 Flask（提高效能）
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
