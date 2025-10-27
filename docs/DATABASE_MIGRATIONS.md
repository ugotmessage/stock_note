# 📊 資料庫遷移管理

## 📋 概述

本專案使用遷移系統來管理資料庫結構變更，確保在不同環境間部署時資料庫結構的一致性。

## 🗂️ 遷移文件結構

```
migrations/
├── 000_initial_schema.sql      # 初始資料庫結構
├── 001_add_ref_fields.sql      # 新增來源欄位
└── ...                         # 未來的遷移文件
```

## 🚀 使用方法

### 執行所有遷移
```bash
python migrate.py
```

### 查看遷移狀態
```bash
python migrate.py status
```

### 在 Docker 中執行遷移
```bash
# 連接到現有資料庫
docker-compose exec python-app python migrate.py

# 獨立部署
docker-compose -f docker-compose.standalone.yml exec python-app python migrate.py
```

## 📝 遷移文件命名規範

- 格式：`XXX_description.sql`
- `XXX`：三位數序號（000, 001, 002...）
- `description`：描述性名稱（使用下劃線分隔）

## 🔧 創建新遷移

1. 在 `migrations/` 資料夾中創建新的 SQL 文件
2. 按照命名規範命名文件
3. 在文件開頭添加註釋說明：
   ```sql
   -- 遷移腳本 XXX: 描述
   -- 日期: YYYY-MM-DD
   -- 描述: 詳細說明
   ```

## 📊 遷移記錄

### 000_initial_schema.sql
- **日期**: 2025-09-16
- **描述**: 建立股票筆記管理系統的初始資料庫結構
- **內容**:
  - 創建 `stocks` 表
  - 創建 `notes` 表（包含來源欄位）
  - 建立索引
  - 插入範例數據

### 001_add_ref_fields.sql
- **日期**: 2025-09-16
- **描述**: 為 notes 表新增 ref (來源) 和 ref_time (來源時間) 欄位
- **內容**:
  - 新增 `ref` 欄位
  - 新增 `ref_time` 欄位
  - 建立相關索引

## ⚠️ 注意事項

1. **備份資料**：執行遷移前請先備份資料庫
2. **測試環境**：先在測試環境中驗證遷移
3. **不可逆操作**：某些遷移可能不可逆，請謹慎操作
4. **依賴順序**：遷移按序號順序執行，請勿跳過序號

## 🔍 故障排除

### 遷移失敗
```bash
# 查看詳細錯誤信息
python migrate.py migrate

# 檢查資料庫連接
python check_database.py
```

### 手動執行遷移
```bash
# 連接到 MySQL
mysql -u username -p stock_note_project

# 執行特定遷移文件
source migrations/000_initial_schema.sql;
```

## 📈 最佳實踐

1. **小步遷移**：每次遷移只做一個小的變更
2. **向後相容**：盡量保持向後相容性
3. **測試驗證**：每次遷移後都要測試功能
4. **文檔記錄**：詳細記錄每個遷移的目的和影響

## 🚀 部署流程

1. **開發環境**：創建和測試遷移
2. **測試環境**：驗證遷移效果
3. **生產環境**：執行遷移部署

```bash
# 1. 檢查遷移狀態
python migrate.py status

# 2. 執行遷移
python migrate.py migrate

# 3. 驗證結果
python migrate.py status
```

