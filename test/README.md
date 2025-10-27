# 測試文件目錄

本目錄包含開發和測試相關的文件。

## 📁 文件說明

### Python 測試腳本

- **test_notes_functionality.py** - 筆記功能測試腳本
  - 測試筆記的增刪改查功能
  - 測試搜尋和排序功能
  
- **db_test.py** - 數據庫連接測試腳本
  - 測試 MySQL 連接
  - 驗證數據庫結構

### HTML 測試頁面

- **test_ajax.html** - AJAX 功能測試頁面
  - 開發時的臨時測試頁面

- **test_header_sort.html** - 表頭排序測試頁面
  - 表格排序功能測試

- **test_styles.html** - 樣式測試頁面
  - CSS 樣式測試

## ⚠️ 注意事項

這些文件僅供開發和測試使用，不應部署到生產環境。

如需運行測試：

```bash
# 功能測試
python test/test_notes_functionality.py

# 數據庫連接測試
python test/db_test.py
```

## 🚀 開發環境

在開發環境中可以直接訪問 HTML 測試頁面：
- http://localhost:5001/test_ajax.html
- http://localhost:5001/test_header_sort.html
- http://localhost:5001/test_styles.html

