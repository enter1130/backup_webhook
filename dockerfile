# 使用 Python 3.9
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製程式碼與 .env 檔案
COPY app.py .
COPY .env .

# 安裝 Flask 和 requests
RUN pip install flask requests python-dotenv

# 開放 5000 端口
EXPOSE 5000

# 啟動 Flask 伺服器
CMD ["python", "app.py"]
