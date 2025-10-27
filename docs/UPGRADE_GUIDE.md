# 🔄 版本升級指南

本文件說明如何從舊版本升級到新版本。

## 📋 升級步驟

### 方法一：使用自動升級腳本（推薦）

專案提供了自動升級腳本，可一鍵完成升級：

```bash
# 執行升級腳本
./scripts/upgrade.sh
```

此腳本會自動執行以下步驟：
1. ✅ 備份數據庫
2. ✅ 更新代碼
3. ✅ 更新依賴
4. ✅ 執行數據庫遷移
5. ✅ 重啟服務
6. ✅ 驗證升級

### 方法二：手動升級

如果需要更多控制，可以手動執行以下步驟：

#### 1. 備份數據庫

```bash
# 使用 mysqldump 備份
mysqldump -u username -p stock_note_project > backup_$(date +%Y%m%d).sql
```

#### 2. 更新代碼

```bash
# 如果使用 Git
git pull

# 或手動上傳新代碼
```

#### 3. 更新依賴

```bash
# 如果是本地環境
pip install -r requirements.txt --upgrade

# 如果是 Docker 環境
docker-compose up -d --build
```

#### 4. 執行數據庫遷移

```bash
# 查看遷移狀態
python migrate.py status

# 執行遷移
python migrate.py migrate
```

#### 5. 重啟服務

```bash
# Docker 環境
docker-compose restart

# 本地環境
# 使用您的進程管理器重啟（如 systemd, supervisor 等）
```

---

## 🐳 Docker 環境升級

### 連接到外部資料庫

```bash
# 1. 備份資料庫
mysqldump -h your_mysql_host -u username -p stock_note_project > backup.sql

# 2. 更新代碼
git pull

# 3. 執行升級腳本
./scripts/upgrade.sh
```

### 獨立部署（包含 MySQL）

```bash
# 1. 備份資料庫
docker exec stock-note-mysql mysqldump -u username -p stock_note_project > backup.sql

# 2. 更新代碼
git pull

# 3. 重新建構並啟動
docker-compose -f docker-compose.standalone.yml up -d --build

# 4. 執行遷移
docker-compose -f docker-compose.standalone.yml exec python-app python migrate.py migrate
```

---

## 🔍 升級檢查清單

升級前請確認：

- [ ] 已備份數據庫
- [ ] 已了解當前版本的新功能
- [ ] 檢查是否有破壞性變更
- [ ] 確認數據庫連接配置正確
- [ ] 確認有足夠的磁碟空間

升級後請驗證：

- [ ] 數據庫連接正常
- [ ] 遷移狀態正確（所有遷移已執行）
- [ ] 應用正常運行
- [ ] 功能測試通過
- [ ] 數據完整性無誤

---

## ⚠️ 常見問題

### 問題 1：升級後數據庫遷移失敗

**解決方案**：
```bash
# 檢查遷移狀態
python migrate.py status

# 查看詳細錯誤
docker-compose logs python-app

# 如果有問題，可以回滾到備份
mysql -u username -p stock_note_project < backup.sql
```

### 問題 2：升級後應用無法啟動

**解決方案**：
```bash
# 檢查容器日誌
docker-compose logs python-app

# 檢查數據庫連接
python check_database.py

# 驗證環境變數
docker-compose exec python-app env | grep MYSQL
```

### 問題 3：升級後功能異常

**解決方案**：
```bash
# 檢查是否所有遷移都已執行
python migrate.py status

# 檢查數據庫結構
mysql -u username -p stock_note_project -e "SHOW TABLES;"
mysql -u username -p stock_note_project -e "DESCRIBE notes;"

# 如果有問題，從備份恢復
mysql -u username -p stock_note_project < backup.sql
```

---

## 🔄 回滾步驟

如果升級失敗，可以回滾到之前的版本：

### 1. 恢復數據庫備份

```bash
# 停止當前服務
docker-compose down

# 恢復數據庫
mysql -u username -p stock_note_project < backup.sql
```

### 2. 還原代碼

```bash
# 如果使用 Git
git checkout <previous-commit-hash>

# 或手動還原文件
```

### 3. 重新啟動服務

```bash
# Docker 環境
docker-compose up -d

# 驗證服務正常
curl http://localhost:5001
```

---

## 📊 升級腳本說明

升級腳本 (`scripts/upgrade.sh`) 會自動執行以下操作：

1. **備份數據庫**：自動創建數據庫備份
2. **更新代碼**：從 Git 拉取最新代碼
3. **更新依賴**：更新 Python 依賴包
4. **執行遷移**：運行未執行的數據庫遷移
5. **重啟服務**：重啟應用服務
6. **驗證升級**：檢查服務是否正常運行

### 使用範例

```bash
# 完整自動升級
./scripts/upgrade.sh

# 只執行遷移
python migrate.py migrate

# 查看遷移狀態
python migrate.py status
```

---

## 🎯 最佳實踐

1. **定期備份**：升級前務必備份數據庫
2. **測試環境**：先在測試環境驗證升級
3. **逐步升級**：不要跳過中間版本直接升級
4. **監控日誌**：升級後監控應用日誌
5. **功能驗證**：升級後測試所有功能

---

## 📞 獲取幫助

如果升級遇到問題：

1. 檢查 [故障排除](#-常見問題) 章節
2. 查看應用日誌：`docker-compose logs`
3. 檢查遷移狀態：`python migrate.py status`
4. 提交 Issue 或聯繫開發團隊

---

## 🔗 相關文檔

- [部署指南](./DEPLOYMENT_GUIDE.md) - 完整部署文檔
- [遷移快速參考](./MIGRATION_QUICK_REF.md) - 常用遷移命令
- [數據庫遷移](./DATABASE_MIGRATIONS.md) - 遷移系統說明

---

**最後更新**：2025-01-XX

