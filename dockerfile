# 使用 Python 3.9
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製程式碼到容器
COPY app.py .
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install -r requirements.txt

# 開放 Render 需要的 Port
EXPOSE 5000

# 啟動 Flask 伺服器（使用 Gunicorn）
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
