# 🔧 修復遷移錯誤指南

## ❌ 常見錯誤

### 錯誤：Duplicate key name

```
❌ 遷移執行失敗: Duplicate key name 'idx_notes_stock_code'
```

**原因**：嘗試創建已存在的索引

**已修正**：現在所有索引創建前都會檢查是否存在

## ✅ 解決方案

### 方法 1：清除特定遷移記錄（推薦）

如果某個遷移失敗了，可以清除它的記錄後重新執行：

```bash
# 清除單個遷移記錄
mysql -u username -p stock_note_project -e "
DELETE FROM migrations WHERE migration_name = '000_initial_schema.sql';
"

# 重新執行遷移
python migrate.py migrate
```

### 方法 2：清除所有遷移記錄

⚠️ **警告**：這會讓所有遷移重新執行

```bash
# 清除所有遷移記錄
mysql -u username -p stock_note_project -e "
DELETE FROM migrations;
"

# 重新執行所有遷移
python migrate.py migrate
```

### 方法 3：手動執行遷移

如果遷移記錄有問題，可以手動執行 SQL：

```bash
# 手動執行遷移 SQL
mysql -u username -p stock_note_project < migrations/000_initial_schema.sql

# 手動記錄遷移
mysql -u username -p stock_note_project -e "
INSERT INTO migrations (migration_name, description) 
VALUES ('000_initial_schema.sql', '手動執行');
"
```

## 🛠️ 故障排除步驟

### 步驟 1：查看當前狀態

```bash
python migrate.py status
```

### 步驟 2：檢查數據庫

```bash
mysql -u username -p stock_note_project -e "
SELECT migration_name, executed_at FROM migrations;
"
```

### 步驟 3：檢查表結構

```bash
mysql -u username -p stock_note_project -e "
SHOW TABLES;
DESCRIBE notes;
"
```

### 步驟 4：檢查索引

```bash
mysql -u username -p stock_note_project -e "
SHOW INDEX FROM notes;
"
```

### 步驟 5：重新執行遷移

```bash
# 方法 A：清除失敗的遷移記錄
mysql -u username -p stock_note_project -e "
DELETE FROM migrations WHERE migration_name = '000_initial_schema.sql';
"
python migrate.py migrate

# 方法 B：直接執行 SQL（跳過檢查）
mysql -u username -p stock_note_project < migrations/000_initial_schema.sql
```

## 📋 正確的遷移流程

### 第一次執行（全新數據庫）

```bash
# 1. 檢查狀態（應該是空的）
python migrate.py status

# 2. 執行遷移
python migrate.py migrate

# 3. 驗證
python migrate.py status
```

### 升級執行（已有數據庫）

```bash
# 1. 檢查狀態
python migrate.py status
# 應該顯示：000_initial_schema.sql: ✅ 已執行

# 2. 執行新遷移
python migrate.py migrate
# 只會執行 001_add_ref_fields.sql

# 3. 驗證
python migrate.py status
```

## 🔍 遷移文件已修正

### 修正內容

✅ **000_initial_schema.sql** - 添加索引存在檢查
✅ **001_add_ref_fields.sql** - 添加欄位存在檢查

現在所有遷移都是**冪等的**（可以安全地重複執行）

## 💡 最佳實踐

1. **備份先行**：執行遷移前先備份數據庫
2. **查看狀態**：執行前先 `python migrate.py status`
3. **測試環境**：先在測試環境驗證
4. **記錄變化**：保留遷移執行記錄

## 🎯 快速修復

如果遇到錯誤，執行以下命令：

```bash
# 1. 清除失敗的遷移記錄
mysql -u username -p stock_note_project -e "
DELETE FROM migrations WHERE migration_name = '000_initial_schema.sql';
"

# 2. 重新執行（現在是安全的）
python migrate.py migrate

# 3. 驗證結果
python migrate.py status
```

