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

## 📋 系統要求

- Python 3.7+
- MySQL 5.7+
- 現代瀏覽器

## 🚀 快速開始

### 1. 克隆項目
```bash
git clone <repository-url>
cd stock_note_project
```

### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

### 3. 配置數據庫
1. 創建MySQL數據庫 `stock_project`
2. 執行以下SQL腳本創建表結構：

```sql
CREATE TABLE IF NOT EXISTS stocks (
    `stock_code` VARCHAR(10) NOT NULL,
    `stock_name` VARCHAR(50) NOT NULL,
    `industry` VARCHAR(50) NULL,
    `last_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS notes (
    `id` INT NOT NULL AUTO_INCREMENT,
    `stock_code` VARCHAR(10) NOT NULL,
    `note_type` ENUM('TAG', 'STORY') NOT NULL,
    `content` TEXT NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`stock_code`) REFERENCES stocks(`stock_code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4. 修改配置
編輯 `config.py` 文件，填入您的MySQL連接信息：

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'stock_project',
    'charset': 'utf8mb4',
    'autocommit': True
}
```

### 5. 啟動應用
```bash
python app.py
```

### 6. 訪問系統
打開瀏覽器訪問: http://localhost:5000

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
