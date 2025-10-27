-- 遷移腳本 001: 新增來源欄位
-- 日期: 2025-09-16
-- 描述: 為 notes 表新增 ref (來源) 和 ref_time (來源時間) 欄位

-- 新增來源欄位（如果不存在）
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
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

-- 新增來源時間欄位（如果不存在）
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
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

-- 為來源欄位建立索引（如果不存在）
SET @index_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
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

-- 為來源時間欄位建立索引（如果不存在）
SET @index_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
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

-- 驗證欄位是否成功新增
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT,
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'stock_note_project' 
    AND TABLE_NAME = 'notes' 
    AND COLUMN_NAME IN ('ref', 'ref_time');

