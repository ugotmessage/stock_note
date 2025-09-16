# 股票筆記管理系統 (Stock Note Management System)

一個基於 Flask 和 MySQL 的股票投資筆記管理系統，支持添加和查看股票相關的標籤和故事筆記。

## 🚀 功能特點

- **股票筆記管理**: 為不同股票添加標籤(TAG)和故事/分析(STORY)筆記
- **自動股票創建**: 當添加新股票代碼的筆記時，系統會自動創建股票記錄
- **現代化UI**: 響應式設計，支持桌面和移動設備
- **實時反饋**: Flash消息提示操作結果
- **數據持久化**: 使用MySQL數據庫存儲所有數據

## 🛠️ 技術架構

- **後端**: Python Flask
- **數據庫**: MySQL
- **前端**: HTML5 + CSS3 + 原生JavaScript
- **模板引擎**: Jinja2

## 🚀 快速開始

### Docker 部署（推薦）

#### 連接到現有資料庫
```bash
# 1. 下載專案
git clone <repository-url>
cd stock_note_project

# 2. 設定環境變數
export MYSQL_HOST=your-mysql-host
export MYSQL_USER=your-username
export MYSQL_PASSWORD=your-password
export MYSQL_DATABASE=stock_note_project

# 3. 啟動應用
docker-compose up -d
```

#### 獨立部署（包含資料庫）
```bash
# 1. 下載專案
git clone <repository-url>
cd stock_note_project

# 2. 一鍵啟動
docker-compose -f docker-compose.standalone.yml up -d
```

### 傳統部署

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 配置資料庫（參考 docs/ 資料夾）
# 3. 啟動應用
python app.py
```

## 📚 詳細文檔

所有詳細的部署和配置說明請參考 `docs/` 資料夾：

### 🚀 部署相關
- **[部署指南](docs/DEPLOYMENT.md)** - Docker 部署完整說明
- **[實體 MySQL 部署](docs/PHYSICAL_MYSQL_DEPLOYMENT.md)** - 連接到實體 MySQL 的設定

### 🔧 功能相關
- **[功能說明](docs/README_NOTES_FEATURES.md)** - 詳細功能介紹

### 🐛 修復記錄
- **[CSS 修復說明](docs/CSS_FIX_SUMMARY.md)** - 樣式修復記錄
- **[AJAX 改進說明](docs/AJAX_IMPROVEMENTS.md)** - AJAX 功能改進記錄

## 🌐 訪問系統

部署完成後，打開瀏覽器訪問: http://localhost:5001

## 📁 項目結構

```
stock_note_project/
├── app.py              # Flask主應用
├── db_manager.py       # 數據庫操作模塊
├── config.py           # 數據庫配置
├── requirements.txt    # Python依賴包
├── README.md          # 項目說明
├── templates/
│   └── index.html     # 主頁模板
└── static/
    └── style.css      # 樣式文件
```

## 🔧 主要功能

### 添加筆記
- 輸入股票代碼（如：2330）
- 選擇筆記類型（TAG 或 STORY）
- 輸入筆記內容
- 系統自動處理股票記錄創建

### 查看筆記
- 按時間倒序顯示所有筆記
- 顯示股票代碼、名稱、類型、內容和創建時間
- 響應式表格設計

## 🎨 UI特性

- 漸變背景設計
- 卡片式佈局
- 懸停效果和動畫
- 移動端適配
- 類型標籤顏色區分

## 🔒 安全特性

- 表單驗證
- SQL注入防護
- 錯誤處理和日誌記錄

## 🚧 開發計劃

- [ ] 用戶認證系統
- [ ] 股票信息自動獲取
- [ ] 筆記搜索和過濾
- [ ] 數據導出功能
- [ ] API接口開發

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 許可證

MIT License

## 📞 聯繫方式

如有問題，請提交 Issue 或聯繫開發團隊。
