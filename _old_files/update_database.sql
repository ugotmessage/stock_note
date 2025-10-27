-- 股票筆記管理系統數據庫更新腳本
-- 為現有的 notes 表添加 updated_at 欄位

USE stock_note_project;

-- 檢查 notes 表是否存在 updated_at 欄位
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND COLUMN_NAME = 'updated_at'
);

-- 如果 updated_at 欄位不存在，則添加它
SET @sql = IF(
    @column_exists = 0,
    'ALTER TABLE notes ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at',
    'SELECT "updated_at 欄位已存在" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 為現有記錄設置 updated_at 值（如果欄位是新添加的）
UPDATE notes SET updated_at = created_at WHERE updated_at IS NULL;

-- 創建 updated_at 索引（如果不存在）
SET @index_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND INDEX_NAME = 'idx_notes_updated_at'
);

SET @index_sql = IF(
    @index_exists = 0,
    'CREATE INDEX idx_notes_updated_at ON notes(updated_at)',
    'SELECT "updated_at 索引已存在" AS message'
);

PREPARE stmt FROM @index_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 顯示更新結果
SELECT '數據庫更新完成！' AS message;
DESCRIBE notes;
