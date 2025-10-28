-- 清除遷移記錄，讓遷移可以重新執行
USE stock_note_project;
DELETE FROM migrations WHERE migration_name = '000_initial_schema.sql';
SELECT '已清除 000_initial_schema.sql 的遷移記錄' AS message;
