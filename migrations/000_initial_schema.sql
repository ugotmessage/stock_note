-- 遷移腳本 000: 初始資料庫結構
-- 日期: 2025-09-16
-- 描述: 建立股票筆記管理系統的初始資料庫結構

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

-- 創建筆記表（包含來源欄位）
CREATE TABLE IF NOT EXISTS notes (
    `id` INT NOT NULL AUTO_INCREMENT,
    `stock_code` VARCHAR(10) NOT NULL,
    `note_type` ENUM('TAG', 'STORY') NOT NULL,
    `content` TEXT NOT NULL,
    `ref` VARCHAR(255) NULL COMMENT '資料來源',
    `ref_time` TIMESTAMP NULL COMMENT '來源時間',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`stock_code`) REFERENCES stocks(`stock_code`) ON DELETE CASCADE,
    INDEX `idx_notes_ref` (`ref`),
    INDEX `idx_notes_ref_time` (`ref_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 創建索引以提高查詢性能
CREATE INDEX idx_notes_stock_code ON notes(stock_code);
CREATE INDEX idx_notes_created_at ON notes(created_at);
CREATE INDEX idx_notes_updated_at ON notes(updated_at);

-- 插入一些範例數據（可選）
INSERT IGNORE INTO stocks (stock_code, stock_name, industry) VALUES
('2330', '台積電', '半導體'),
('2317', '鴻海', '電子製造'),
('2454', '聯發科', '半導體'),
('2881', '富邦金', '金融保險'),
('2882', '國泰金', '金融保險');

-- 插入一些範例筆記（可選）
INSERT IGNORE INTO notes (stock_code, note_type, content, ref, ref_time) VALUES
('2330', 'TAG', 'AI 晶片龍頭', '財經新聞', '2025-09-16 10:00:00'),
('2330', 'STORY', '台積電在 AI 晶片市場的優勢分析...', '研究報告', '2025-09-16 11:00:00'),
('2317', 'TAG', 'iPhone 組裝', '財經新聞', '2025-09-16 12:00:00');

