import os
import sys
import argparse
from typing import Optional

try:
	import mysql.connector
	from mysql.connector import Error
except Exception as import_error:
	print(f"[ERROR] 無法匯入 mysql-connector-python，請先安裝: pip install mysql-connector-python\n詳細: {import_error}")
	sys.exit(2)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="MySQL 連線測試工具")
	parser.add_argument("--host", default=os.getenv("DB_HOST", "mysql"), help="MySQL 主機名稱或 IP")
	parser.add_argument("--port", type=int, default=int(os.getenv("DB_PORT", "3306")), help="MySQL 連線埠")
	parser.add_argument("--user", default=os.getenv("DB_USER", "snote"), help="MySQL 使用者")
	parser.add_argument("--password", default=os.getenv("DB_PASSWORD", ")EkxSYA9YJFu(i)a"), help="MySQL 密碼")
	parser.add_argument("--database", default=os.getenv("DB_NAME", "stock_note_project"), help="要檢查的資料庫名稱")
	parser.add_argument("--timeout", type=int, default=8, help="連線逾時秒數")
	return parser.parse_args()


def connect_mysql(host: str, port: int, user: str, password: str, database: Optional[str], timeout: int):
	connection = mysql.connector.connect(
		host=host,
		port=port,
		user=user,
		password=password,
		database=database,
		charset="utf8mb4",
		connection_timeout=timeout,
		autocommit=True,
	)
	return connection


def main() -> int:
	args = parse_args()

	print("== MySQL 連線測試 ==")
	print(f"Host: {args.host}:{args.port}")
	print(f"User: {args.user}")
	print(f"Database: {args.database}")

	try:
		conn = connect_mysql(
			host=args.host,
			port=args.port,
			user=args.user,
			password=args.password,
			database=args.database,
			timeout=args.timeout,
		)
		cursor = conn.cursor()

		# 測試基本查詢
		cursor.execute("SELECT 1")
		_ = cursor.fetchone()

		# 伺服器版本
		cursor.execute("SELECT VERSION()")
		version_row = cursor.fetchone()
		print(f"Server Version: {version_row[0] if version_row else 'Unknown'}")

		# 確認目前資料庫
		cursor.execute("SELECT DATABASE()")
		db_row = cursor.fetchone()
		print(f"Current Database: {db_row[0] if db_row and db_row[0] else '(無)'}")

		# 檢查必要資料表
		required_tables = ["stocks", "notes"]
		missing_tables = []
		for table in required_tables:
			cursor.execute("SHOW TABLES LIKE %s", (table,))
			if cursor.fetchone() is None:
				missing_tables.append(table)

		if missing_tables:
			print(f"[WARN] 缺少資料表: {', '.join(missing_tables)}")
			print("      請先建立資料表 (參考您的 schema SQL)。")
		else:
			print("[OK] 所有必要資料表已存在: stocks, notes")

		print("[SUCCESS] MySQL 連線與基本檢查成功。")
		return 0

	except Error as e:
		print(f"[ERROR] 無法連線或查詢 MySQL: {e}")
		print("排查建議:\n- 確認容器/服務是否運行，且與此腳本同網路可達\n- 若以 Docker：確認 python 與 mysql 在同一個 network，且 MySQL 容器名稱/別名為 'mysql'\n- 檢查使用者/密碼/資料庫名稱是否正確\n- 嘗試: mysql -h <host> -u <user> -p 連線測試")
		return 1
	finally:
		try:
			if 'cursor' in locals():
				cursor.close()
			if 'conn' in locals() and conn.is_connected():
				conn.close()
		except Exception:
			pass


if __name__ == "__main__":
	sys.exit(main())
