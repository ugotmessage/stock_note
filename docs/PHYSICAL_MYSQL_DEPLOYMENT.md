# 🚀 實體 MySQL 部署指南

## 📋 情境說明

當您要在有實體安裝 MySQL 的主機上部署此應用時，需要正確配置 Docker 容器與實體 MySQL 的連接。

## 🔧 設定方法

### 方法 1: 使用 host.docker.internal（推薦）

適用於：MySQL 在同一台主機上運行

#### 1. 創建環境變數文件
創建 `.env` 文件：
```bash
# 資料庫配置
MYSQL_HOST=host.docker.internal
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=stock_note_project

# Flask 配置
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

#### 2. 啟動應用
```bash
docker-compose up -d
```

### 方法 2: 使用主機 IP 地址

適用於：MySQL 在不同主機上運行

#### 1. 創建環境變數文件
創建 `.env` 文件：
```bash
# 資料庫配置
MYSQL_HOST=192.168.1.100  # 替換為實際的 MySQL 主機 IP
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=stock_note_project

# Flask 配置
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

#### 2. 啟動應用
```bash
docker-compose up -d
```

### 方法 3: 使用 Docker 網路模式

適用於：需要更精確的網路控制

#### 1. 修改 docker-compose.yml
```yaml
version: '3.8'

services:
  python-app:
    build:
      context: .
      dockerfile: Dockerfile
    image: stock-note-app:latest
    container_name: stock-note-app
    working_dir: /app
    volumes:
      - .:/app
    ports:
      - "5001:5000"
    network_mode: "host"  # 使用主機網路模式
    environment:
      - MYSQL_HOST=localhost
      - MYSQL_PORT=3306
      - MYSQL_USER=your_mysql_username
      - MYSQL_PASSWORD=your_mysql_password
      - MYSQL_DATABASE=stock_note_project
      - FLASK_APP=app.py
      - FLASK_ENV=production
    restart: unless-stopped
```

#### 2. 啟動應用
```bash
docker-compose up -d
```

## 🔍 故障排除

### 1. 連接測試
在容器內測試 MySQL 連接：
```bash
# 進入容器
docker-compose exec python-app bash

# 測試連接
python -c "
import mysql.connector
from config import DB_CONFIG
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print('MySQL 連接成功！')
    conn.close()
except Exception as e:
    print(f'連接失敗: {e}')
"
```

### 2. 檢查 MySQL 配置
確保 MySQL 允許外部連接：

#### 檢查 MySQL 綁定地址
```sql
-- 在 MySQL 中執行
SHOW VARIABLES LIKE 'bind_address';
```

如果顯示 `127.0.0.1`，需要修改為 `0.0.0.0`：
```bash
# 編輯 MySQL 配置文件
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# 修改 bind-address
bind-address = 0.0.0.0

# 重啟 MySQL
sudo systemctl restart mysql
```

#### 檢查用戶權限
```sql
-- 創建用戶並授權
CREATE USER 'snote'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON stock_note_project.* TO 'snote'@'%';
FLUSH PRIVILEGES;
```

### 3. 防火牆設定
確保 MySQL 端口開放：
```bash
# Ubuntu/Debian
sudo ufw allow 3306

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
```

## 📊 部署檢查清單

- [ ] MySQL 服務正在運行
- [ ] MySQL 允許外部連接（bind-address = 0.0.0.0）
- [ ] 用戶權限正確設定
- [ ] 防火牆端口開放
- [ ] 資料庫和表已創建
- [ ] 環境變數正確設定
- [ ] Docker 容器可以連接到 MySQL

## 🚀 快速部署命令

```bash
# 1. 下載專案
git clone <repository-url>
cd stock_note_project

# 2. 創建環境變數文件
cat > .env << EOF
MYSQL_HOST=host.docker.internal
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=stock_note_project
EOF

# 3. 啟動應用
docker-compose up -d

# 4. 檢查狀態
docker-compose ps
docker-compose logs python-app
```

## 📞 常見問題

### Q: 容器無法連接到 MySQL
A: 檢查 MySQL 的 bind-address 設定和用戶權限

### Q: 連接被拒絕
A: 確認防火牆設定和 MySQL 服務狀態

### Q: 認證失敗
A: 檢查用戶名和密碼是否正確

### Q: 資料庫不存在
A: 先執行 `init_database.sql` 創建資料庫和表
