-- 股票筆記管理系統數據庫初始化腳本
-- 請在MySQL中執行此腳本來創建所需的數據庫和表

-- 創建數據庫
CREATE DATABASE IF NOT EXISTS stock_note_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用數據庫
USE stock_note_project;

-- 創建股票表
CREATE TABLE IF NOT EXISTS stocks (
    `stock_code` VARCHAR(10) NOT NULL,
    `stock_name` VARCHAR(50) NOT NULL,
    `industry` VARCHAR(50) NULL,
    `last_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 創建筆記表
CREATE TABLE IF NOT EXISTS notes (
    `id` INT NOT NULL AUTO_INCREMENT,
    `stock_code` VARCHAR(10) NOT NULL,
    `note_type` ENUM('TAG', 'STORY') NOT NULL,
    `content` TEXT NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`stock_code`) REFERENCES stocks(`stock_code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 創建索引以提高查詢性能
CREATE INDEX idx_notes_stock_code ON notes(stock_code);
CREATE INDEX idx_notes_created_at ON notes(created_at);
CREATE INDEX idx_notes_updated_at ON notes(updated_at);
CREATE INDEX idx_notes_type ON notes(note_type);

-- 插入一些示例數據（可選）
INSERT INTO stocks (stock_code, stock_name, industry) VALUES 
('2330', '台積電', '半導體'),
('2317', '鴻海', '電子製造'),
('2454', '聯發科', '半導體')
ON DUPLICATE KEY UPDATE stock_name = VALUES(stock_name);

INSERT INTO notes (stock_code, note_type, content) VALUES 
('2330', 'TAG', '護國神山，技術領先'),
('2330', 'STORY', '台積電在先進製程技術上持續領先，是台灣最重要的科技公司之一。'),
('2317', 'TAG', '代工龍頭'),
('2317', 'STORY', '鴻海是全球最大的電子製造服務商，在iPhone等產品製造中扮演關鍵角色。'),
('2454', 'TAG', '手機晶片大廠'),
('2454', 'STORY', '聯發科在手機晶片市場佔有重要地位，特別是在中低端市場表現優異。')
ON DUPLICATE KEY UPDATE content = VALUES(content);

-- 顯示創建結果
SELECT '數據庫 stock_note_project 創建成功！' AS message;
SELECT 'stocks 表創建成功！' AS message;
SELECT 'notes 表創建成功！' AS message;

-- 顯示表結構
DESCRIBE stocks;
DESCRIBE notes;

-- 顯示示例數據
SELECT 'stocks 表示例數據:' AS message;
SELECT * FROM stocks;

SELECT 'notes 表示例數據:' AS message;
SELECT * FROM notes;
