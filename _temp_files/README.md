# 臨時文件目錄

此目錄包含在開發和調試過程中使用的臨時文件。

## 📁 文件說明

- **check_schema.py** - 數據庫結構檢查腳本
- **verify_migration.py** - 遷移驗證腳本
- **clear_migrations.sql** - 清除遷移記錄的 SQL
- **online_fix.sql** - 線上數據庫修復 SQL

## ⚠️ 注意

這些文件僅用於調試和一次性任務，不需要部署到生產環境。

如果需要使用這些文件，請檢查其內容是否仍然適用。

## 🗑️ 清理建議

如果專案已經穩定運行，可以考慮刪除此目錄：

```bash
rm -rf _temp_files
```

