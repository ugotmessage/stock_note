# 🚀 Docker 部署指南

## 📋 系統要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用記憶體
- 至少 5GB 可用磁碟空間

## 🚀 部署選項

### 選項 1: 連接到現有資料庫（推薦）

如果您已經有 MySQL 資料庫，使用此選項：

#### 1. 下載專案
```bash
git clone <repository-url>
cd stock_note_project
```

#### 2. 設定環境變數
```bash
# 複製環境變數範本
cp env.example .env

# 編輯 .env 文件，填入您的資料庫資訊
nano .env
```

**必要的環境變數：**
```bash
MYSQL_HOST=your-mysql-host
MYSQL_USER=your-username
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=stock_note_project
```

#### 3. 啟動應用
```bash
docker-compose up -d
```

### 選項 2: 獨立部署（包含資料庫）

如果您沒有現有的 MySQL 資料庫，使用此選項：

#### 1. 下載專案
```bash
git clone <repository-url>
cd stock_note_project
```

#### 2. 設定環境變數
```bash
# 複製環境變數範本
cp env.example .env

# 編輯 .env 文件，設定所有必要的環境變數
nano .env
```

**必要的環境變數：**
```bash
MYSQL_HOST=mysql
MYSQL_USER=your-username
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=stock_note_project
MYSQL_ROOT_PASSWORD=your-root-password
```

#### 3. 一鍵啟動（包含 MySQL）
```bash
docker-compose -f docker-compose.standalone.yml up -d
```

### 3. 檢查服務狀態
```bash
docker-compose ps
```

### 4. 查看日誌
```bash
# 查看所有服務日誌
docker-compose logs

# 查看特定服務日誌
docker-compose logs python-app
docker-compose logs mysql
```

### 5. 訪問應用
打開瀏覽器訪問: http://localhost:5001

## 🔧 進階配置

### 修改資料庫密碼
1. 編輯 `docker-compose.yml` 文件
2. 修改 `MYSQL_PASSWORD` 和 `MYSQL_ROOT_PASSWORD` 環境變數
3. 重新啟動服務：
```bash
docker-compose down
docker-compose up -d
```

### 修改應用程式端口
編輯 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:5000"  # 將 8080 改為您想要的端口
```

### 資料持久化
- MySQL 資料會自動保存到 Docker volume `mysql_data`
- 即使容器重啟，資料也不會丟失

## 🛠️ 管理命令

### 停止服務
```bash
docker-compose down
```

### 重新構建並啟動
```bash
docker-compose up -d --build
```

### 清理所有資料（⚠️ 會刪除所有資料）
```bash
docker-compose down -v
```

### 進入容器除錯
```bash
# 進入 Python 應用容器
docker-compose exec python-app bash

# 進入 MySQL 容器
docker-compose exec mysql mysql -u snote -p
```

## 🔍 故障排除

### 1. 端口被佔用
```bash
# 檢查端口使用情況
netstat -tulpn | grep :5001
netstat -tulpn | grep :3306

# 修改 docker-compose.yml 中的端口映射
```

### 2. 資料庫連接失敗
```bash
# 檢查 MySQL 容器狀態
docker-compose logs mysql

# 檢查網路連接
docker-compose exec python-app ping mysql
```

### 3. 應用程式無法啟動
```bash
# 查看詳細錯誤日誌
docker-compose logs python-app

# 檢查依賴安裝
docker-compose exec python-app pip list
```

## 📊 監控和維護

### 查看資源使用情況
```bash
docker stats
```

### 備份資料庫
```bash
# 創建備份
docker-compose exec mysql mysqldump -u snote -p stock_note_project > backup.sql

# 恢復備份
docker-compose exec -T mysql mysql -u snote -p stock_note_project < backup.sql
```

### 更新應用程式
```bash
# 拉取最新代碼
git pull

# 重新構建並啟動
docker-compose up -d --build
```

## 🌐 生產環境部署

### 1. 修改安全配置
- 更改預設密碼
- 設定強密碼
- 配置防火牆規則

### 2. 使用 HTTPS
- 配置反向代理（如 Nginx）
- 申請 SSL 證書

### 3. 監控和日誌
- 配置日誌收集
- 設定監控警報
- 定期備份資料

## 📞 支援

如遇到問題，請檢查：
1. Docker 和 Docker Compose 版本
2. 系統資源使用情況
3. 網路連接狀態
4. 容器日誌輸出

更多技術支援，請提交 Issue 或聯繫開發團隊。
