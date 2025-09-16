# 數據庫配置文件
# 支援環境變數配置，方便 Docker 部署和外部資料庫連接

import os

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),        # MySQL主機地址
    'port': int(os.getenv('MYSQL_PORT', '3306')),        # MySQL端口
    'user': os.getenv('MYSQL_USER', 'snote'),            # MySQL用戶名
    'password': os.getenv('MYSQL_PASSWORD', ')EkxSYA9YJFu(i)a'), # MySQL密碼
    'database': os.getenv('MYSQL_DATABASE', 'stock_note_project'), # 數據庫名稱
    'charset': 'utf8mb4',
    'autocommit': True
}
