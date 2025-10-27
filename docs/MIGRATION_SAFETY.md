# 🔒 數據庫遷移安全性說明

## ✅ 安全性保證

### 不會覆蓋現有數據

遷移系統設計為**增量更新**，不會覆蓋或刪除現有數據。安全機制包括：

#### 1. **智能跳過機制**
```python
# migrate.py 會跳過已執行的遷移
if migration_name in executed_migrations:
    print(f"⏭️ 跳過已執行的遷移: {migration_name}")
    continue
```

#### 2. **安全 SQL 語句**

所有遷移使用安全的語法：

```sql
-- 使用 IF NOT EXISTS 避免重複創建
CREATE TABLE IF NOT EXISTS notes (...);

-- 使用 INSERT IGNORE 避免重複插入
INSERT IGNORE INTO stocks VALUES (...);

-- 檢查後再添加欄位
SET @column_exists = (SELECT COUNT(*) FROM ...);
IF @column_exists = 0 THEN
    ALTER TABLE ... ADD COLUMN ...
END IF;
```

#### 3. **事務保護**

如果遷移失敗，會自動回滾：

```python
try:
    # 執行遷移
    cursor.execute(statement)
except Error as e:
    connection.rollback()  # 失敗時回滾
```

## 📋 遷移文件解析

### 000_initial_schema.sql

**目的**：創建初始表結構

**安全措施**：
- ✅ `CREATE DATABASE IF NOT EXISTS` - 不會覆蓋現有數據庫
- ✅ `CREATE TABLE IF NOT EXISTS` - 不會覆蓋現有表
- ✅ `INSERT IGNORE` - 不會覆蓋現有數據

**執行條件**：
- 只在數據庫全新安裝時執行
- 如果表已存在且有數據，只會創建缺失的表
- 範例數據只在空表時插入

### 001_add_ref_fields.sql

**目的**：新增 `ref` 和 `ref_time` 欄位

**安全措施**：
- ✅ 檢查欄位是否存在後再添加
- ✅ 檢查索引是否存在後再創建
- ✅ 只在欄位不存在時執行 `ALTER TABLE`

**執行條件**：
- 自動檢查欄位是否已存在
- 如果欄位已存在，跳過並顯示 "欄位已存在"
- 不會修改現有欄位的值

## 🎯 實際執行流程

### 場景 1：全新數據庫

```bash
python migrate.py migrate
```

**執行過程**：
1. ✅ 創建數據庫（如果不存在）
2. ✅ 創建 tables（如果不存在）
3. ✅ 插入範例數據（使用 INSERT IGNORE）
4. ✅ 新增欄位和索引
5. ✅ 記錄到 migrations 表

**結果**：乾淨的數據庫，帶有範例數據

### 場景 2：已有數據庫

```bash
python migrate.py migrate
```

**執行過程**：
1. ✅ 檢查 migrations 表
2. ✅ 跳過已執行的遷移
3. ✅ 只執行新的遷移
4. ✅ 使用安全語句不覆蓋現有數據

**結果**：數據庫結構更新，現有數據保留

### 場景 3：部分執行的遷移

```bash
python migrate.py migrate
```

**執行過程**：
1. ✅ 讀取 migrations 表已執行列表
2. ✅ 跳過 000（已執行）
3. ✅ 執行 001（新增欄位，檢查後再添加）
4. ✅ 記錄 001 為已執行

**結果**：新增欄位，不影響現有數據

## 🔍 檢查遷移狀態

### 查看遷移記錄

```bash
python migrate.py status
```

**輸出範例**：
```
📊 遷移狀態:
已執行: 2 個
總計: 2 個
  000_initial_schema.sql: ✅ 已執行
  001_add_ref_fields.sql: ✅ 已執行
```

### 查看數據庫中的遷移記錄

```sql
-- 查看已執行的遷移
SELECT * FROM migrations ORDER BY executed_at;

-- 輸出：
-- id | migration_name           | executed_at       | description
-- 1  | 000_initial_schema.sql   | 2025-01-XX 10:00 | 初始結構
-- 2  | 001_add_ref_fields.sql   | 2025-01-XX 10:05 | 新增來源欄位
```

## ⚠️ 注意事項

### 1. 建議備份
雖然遷移系統很安全，但建議在執行前備份：

```bash
mysqldump -u username -p stock_note_project > backup.sql
```

### 2. 測試環境
先在測試環境驗證遷移：

```bash
# 在測試環境執行
python migrate.py status
python migrate.py migrate
```

### 3. 查看日誌
遷移執行過程會顯示詳細日誌：

```bash
python migrate.py migrate

# 輸出範例：
# ✅ 遷移記錄表已創建或已存在
# 📋 已執行的遷移: ['000_initial_schema.sql']
# 🔄 執行遷移: 001_add_ref_fields.sql
# ✅ 遷移執行成功: 001_add_ref_fields.sql
```

## 🎉 總結

**遷移系統不會覆蓋現有數據**，因為：

1. ✅ 使用 `IF NOT EXISTS` 語句
2. ✅ 智能跳過已執行的遷移
3. ✅ 檢查後再執行 `ALTER TABLE`
4. ✅ 使用 `INSERT IGNORE` 避免重複插入
5. ✅ 失敗時自動回滾

**可以放心執行**：
```bash
python migrate.py migrate
```

