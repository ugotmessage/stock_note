-- 遷移腳本 001: 新增來源欄位
-- 日期: 2025-09-16
-- 描述: 為 notes 表新增 ref (來源) 和 ref_time (來源時間) 欄位

-- 新增來源欄位
ALTER TABLE notes 
ADD COLUMN ref VARCHAR(255) NULL COMMENT '資料來源';

-- 新增來源時間欄位
ALTER TABLE notes 
ADD COLUMN ref_time TIMESTAMP NULL COMMENT '來源時間';

-- 為來源欄位建立索引以提升查詢效能
CREATE INDEX idx_notes_ref ON notes(ref);

-- 為來源時間欄位建立索引
CREATE INDEX idx_notes_ref_time ON notes(ref_time);

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

