-- ======================================================
-- 線上數據庫修復 SQL
-- 直接執行此腳本新增缺失的欄位
-- ======================================================

USE stock_note_project;

-- ======================================================
-- 1. 新增 ref 欄位（如果不存在）
-- ======================================================
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND COLUMN_NAME = 'ref'
);

SET @sql = IF(
    @column_exists = 0,
    'ALTER TABLE notes ADD COLUMN ref VARCHAR(255) NULL COMMENT ''資料來源''',
    'SELECT ''ref 欄位已存在'' AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ======================================================
-- 2. 新增 ref_time 欄位（如果不存在）
-- ======================================================
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND COLUMN_NAME = 'ref_time'
);

SET @sql = IF(
    @column_exists = 0,
    'ALTER TABLE notes ADD COLUMN ref_time TIMESTAMP NULL COMMENT ''來源時間''',
    'SELECT ''ref_time 欄位已存在'' AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ======================================================
-- 3. 新增 ref 索引（如果不存在）
-- ======================================================
SET @index_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND INDEX_NAME = 'idx_notes_ref'
);

SET @sql = IF(
    @index_exists = 0,
    'CREATE INDEX idx_notes_ref ON notes(ref)',
    'SELECT ''idx_notes_ref 索引已存在'' AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ======================================================
-- 4. 新增 ref_time 索引（如果不存在）
-- ======================================================
SET @index_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND INDEX_NAME = 'idx_notes_ref_time'
);

SET @sql = IF(
    @index_exists = 0,
    'CREATE INDEX idx_notes_ref_time ON notes(ref_time)',
    'SELECT ''idx_notes_ref_time 索引已存在'' AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ======================================================
-- 5. 驗證結果
-- ======================================================
SELECT '完成！檢查結果：' AS message;

SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'stock_note_project' 
    AND TABLE_NAME = 'notes' 
    AND COLUMN_NAME IN ('ref', 'ref_time');

SELECT 
    INDEX_NAME,
    COLUMN_NAME
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'stock_note_project'
    AND TABLE_NAME = 'notes'
    AND INDEX_NAME IN ('idx_notes_ref', 'idx_notes_ref_time');

-- ======================================================
-- 完成！如果欄位已存在，會顯示 "已存在" 訊息
-- 如果欄位不存在，會自動新增
-- ======================================================

