# 使用更兼容的Python 3.8鏡像
FROM python:3.8-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 暴露端口
EXPOSE 5000

# 設置環境變量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 在容器啟動時再安裝依賴（依賴於掛載進來的程式碼）
CMD ["/bin/sh", "-c", "pip install --no-cache-dir -r requirements.txt && python app.py"]

