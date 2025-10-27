# 🚀 部署與遷移指南

本文件說明如何將股票筆記管理系統部署到新的主機並執行數據庫遷移。

## 📋 目錄

- [前置需求](#前置需求)
- [部署準備](#部署準備)
- [數據庫遷移流程](#數據庫遷移流程)
- [Docker 部署](#docker-部署)
- [手動部署](#手動部署)
- [故障排除](#故障排除)

---

## 前置需求

### 系統需求
- Python 3.8+
- MySQL 5.7+ 或 MariaDB 10.3+
- Docker 和 Docker Compose（如果使用 Docker 部署）

### 網路需求
- 主機可連接到 MySQL 數據庫
- 如果使用外部數據庫，確保防火牆允許連接

---

## 部署準備

### 1. 準備專案文件

```bash
# 複製專案到目標主機
git clone <repository_url> stock_note_project
cd stock_note_project

# 或者使用 scp 上傳專案文件
scp -r stock_note_project user@target_host:/path/to/destination
```

### 2. 設定環境變數

創建 `.env` 文件（基於 `env.example`）：

```bash
cp env.example .env
```

編輯 `.env` 文件，填入資料庫連接資訊：

```ini
# 資料庫配置
MYSQL_HOST=your_mysql_host         # 資料庫主機地址
MYSQL_PORT=3306                    # 資料庫端口
MYSQL_USER=your_username           # 資料庫用戶名
MYSQL_PASSWORD=your_password       # 資料庫密碼
MYSQL_DATABASE=stock_note_project  # 資料庫名稱

# Flask 配置
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

### 3. 安裝依賴

如果使用 Docker，跳到 [Docker 部署](#docker-部署) 章節。

如果手動部署：

```bash
# 創建虛擬環境（建議）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安裝 Python 依賴
pip install -r requirements.txt
```

---

## 數據庫遷移流程

專案使用自動化遷移系統管理數據庫結構變更。

### 遷移文件結構

```
migrations/
├── 000_initial_schema.sql  # 初始數據庫結構
└── 001_add_ref_fields.sql  # 新增來源欄位
```

### 方法一：使用遷移腳本（推薦）

```bash
# 1. 檢查遷移狀態
python migrate.py status

# 2. 執行所有未執行的遷移
python migrate.py migrate

# 3. 再次檢查狀態以確認
python migrate.py status
```

### 方法二：手動執行遷移

如果遷移腳本無法正常工作，可以手動執行：

```bash
# 連接 MySQL
mysql -u your_username -p your_database

# 執行遷移文件
source migrations/000_initial_schema.sql;
source migrations/001_add_ref_fields.sql;
```

### 方法三：使用 init_database.sql

如果數據庫完全沒有建立，可以使用初始化腳本：

```bash
mysql -u root -p < init_database.sql
```

⚠️ **注意**：`init_database.sql` 會創建數據庫和插入範例數據。

---

## Docker 部署

### 連接到現有數據庫

如果你已經有 MySQL 數據庫：

```bash
# 1. 設定環境變數（在 .env 文件中）
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=stock_note_project

# 2. 確保 Docker network 已創建
docker network create my-network

# 3. 啟動服務
docker-compose up -d

# 4. 執行數據庫遷移
docker-compose exec python-app python migrate.py migrate
```

### 獨立部署（包含 MySQL）

如果你想在同一主機上部署包含 MySQL 的完整系統：

```bash
# 1. 設定 .env 文件（包含 MYSQL_ROOT_PASSWORD）

# 2. 啟動服務
docker-compose -f docker-compose.standalone.yml up -d

# 3. 等待 MySQL 就緒
sleep 10

# 4. 執行數據庫初始化
docker-compose -f docker-compose.standalone.yml exec python-app python migrate.py migrate
```

---

## 手動部署

### 1. 初始化數據庫

```bash
# 連接 MySQL
mysql -u root -p

# 創建數據庫（如果需要）
CREATE DATABASE IF NOT EXISTS stock_note_project 
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 執行遷移

```bash
# 使用遷移腳本
python migrate.py migrate

# 或手動執行
mysql -u your_username -p stock_note_project < migrations/000_initial_schema.sql
mysql -u your_username -p stock_note_project < migrations/001_add_ref_fields.sql
```

### 3. 啟動應用

```bash
# 使用 Flask 開發服務器（僅測試用）
export FLASK_APP=app.py
python app.py

# 或使用生產環境 WSGI 服務器（推薦）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 遷移系統說明

### 工作原理

1. **遷移記錄表**：系統在數據庫中創建 `migrations` 表來記錄已執行的遷移
2. **自動追蹤**：每次執行遷移時，系統會檢查哪些遷移已執行
3. **順序執行**：遷移按文件名的數字順序執行（000, 001, 002...）

### 查看遷移狀態

```bash
python migrate.py status
```

輸出範例：
```
📊 遷移狀態:
已執行: 2 個
總計: 2 個
  000_initial_schema.sql: ✅ 已執行
  001_add_ref_fields.sql: ✅ 已執行
```

### 遷移記錄表結構

```sql
CREATE TABLE migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);
```

---

## 完整部署流程

### 情境 A：全新部署到新主機

```bash
# 1. 上傳專案文件到目標主機
scp -r stock_note_project user@host:/opt/

# 2. SSH 到目標主機
ssh user@host

# 3. 進入專案目錄
cd /opt/stock_note_project

# 4. 設定環境變數
cp env.example .env
vi .env  # 編輯資料庫連接資訊

# 5. 確保 MySQL 可用
mysql -h your_host -u your_user -p -e "SELECT 1"

# 6. 如果是 Docker 部署
docker-compose up -d
docker-compose exec python-app python migrate.py migrate

# 7. 驗證部署
curl http://localhost:5001
```

### 情境 B：從舊主機遷移到新主機

```bash
# 步驟 1：在舊主機上備份數據庫
mysqldump -u username -p stock_note_project > backup.sql

# 步驟 2：將備份傳輸到新主機
scp backup.sql user@new_host:/tmp/

# 步驟 3：在新主機上部署應用（參考情境 A 的步驟 1-5）

# 步驟 4：在新主機上導入數據
mysql -u username -p stock_note_project < /tmp/backup.sql

# 步驟 5：執行遷移（確保數據庫結構是最新的）
python migrate.py migrate

# 步驟 6：驗證數據
python check_database.py
```

---

## 故障排除

### 問題 1：遷移失敗 - 資料庫連接錯誤

**解決方案**：
```bash
# 檢查環境變數
env | grep MYSQL

# 測試數據庫連接
python check_database.py

# 檢查配置文件
cat config.py
```

### 問題 2：遷移已存在但未執行

**解決方案**：
```bash
# 查看已執行的遷移
mysql -u username -p -e "SELECT * FROM migrations;"

# 手動執行遷移
python migrate.py migrate
```

### 問題 3：Docker 容器無法連接到外部 MySQL

**解決方案**：
```bash
# 檢查 Docker network
docker network ls
docker network inspect my-network

# 確保數據庫允許外部連接
# 在 MySQL 服務器上執行：
GRANT ALL PRIVILEGES ON stock_note_project.* TO 'your_user'@'%' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
```

### 問題 4：字符編碼問題

**解決方案**：
```sql
-- 確保數據庫使用正確的字符集
ALTER DATABASE stock_note_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 檢查表字符集
SHOW TABLE STATUS FROM stock_note_project;
```

---

## 最佳實踐

1. **備份先行**：執行遷移前務必備份數據庫
2. **測試環境**：先在測試環境驗證遷移
3. **逐步遷移**：小步快跑，每次遷移只做一個變更
4. **版本控制**：將遷移文件納入 Git 版本控制
5. **文檔記錄**：詳細記錄每個遷移的目的和影響

---

## 相關文件

- [遷移管理文檔](./DATABASE_MIGRATIONS.md)
- [部署文檔](./DEPLOYMENT.md)
- [實體 MySQL 部署](./PHYSICAL_MYSQL_DEPLOYMENT.md)

---

## 支援與協助

如果遇到問題，請檢查：

1. 數據庫連接是否正常：`python check_database.py`
2. 遷移狀態：`python migrate.py status`
3. 系統日誌：`docker-compose logs`
4. 網絡連接：`ping your_mysql_host`

---

**最後更新**：2025-01-XX

