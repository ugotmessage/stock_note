# 🔄 數據庫遷移快速參考

## 基本命令

### 查看遷移狀態
```bash
python migrate.py status
```

### 執行所有未完成的遷移
```bash
python migrate.py migrate
```

### 在 Docker 中執行遷移
```bash
# 方法 1：使用命令
docker-compose exec python-app python migrate.py

# 方法 2：使用快捷腳本
./scripts/migrate_in_docker.sh

# 獨立部署
docker-compose -f docker-compose.standalone.yml exec python-app python migrate.py
```

## 常用場景

### 場景 1：部署到新主機（乾淨資料庫）
```bash
# 1. 匯入初始結構
mysql -u username -p stock_note_project < migrations/000_initial_schema.sql

# 2. 執行其他遷移
python migrate.py migrate
```

### 場景 2：從備份恢復後執行遷移
```bash
# 1. 恢復備份
mysql -u username -p stock_note_project < backup.sql

# 2. 執行遷移確保結構最新
python migrate.py migrate
```

### 場景 3：檢查遷移是否有問題
```bash
# 1. 查看狀態
python migrate.py status

# 2. 測試連接
python check_database.py

# 3. 檢查數據庫結構
mysql -u username -p stock_note_project -e "SHOW TABLES;"
```

## 遷移文件位置
```
migrations/
├── 000_initial_schema.sql  # 初始結構
└── 001_add_ref_fields.sql  # 添加來源欄位
```

## 遷移記錄表
```sql
-- 查看已執行的遷移
SELECT * FROM migrations ORDER BY executed_at;

-- 重置遷移（僅開發環境）
-- 警告：不要在主機上執行此操作！
DELETE FROM migrations;
```

## 故障排除

### 錯誤：遷移已存在但未記錄
```bash
# 手動記錄遷移
mysql -u username -p stock_note_project
INSERT INTO migrations (migration_name, description) 
VALUES ('001_add_ref_fields.sql', '手動記錄');
```

### 錯誤：連接失敗
```bash
# 檢查環境變數
env | grep MYSQL

# 檢查配置
python check_database.py
```

## 備份命令
```bash
# 備份整個數據庫
mysqldump -u username -p stock_note_project > backup.sql

# 只備份結構
mysqldump -u username -p --no-data stock_note_project > schema.sql

# 只備份數據
mysqldump -u username -p --no-create-info stock_note_project > data.sql
```

## 快速檢查清單
- [ ] 數據庫連接正常 (`python check_database.py`)
- [ ] 查看當前遷移狀態 (`python migrate.py status`)
- [ ] 執行遷移 (`python migrate.py migrate`)
- [ ] 驗證遷移結果 (`python migrate.py status`)

---

**完整文檔**：請參考 [部署與遷移指南](./DEPLOYMENT_GUIDE.md)

