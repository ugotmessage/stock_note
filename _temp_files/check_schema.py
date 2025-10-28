import mysql.connector
from config import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

print("=== notes 表結構 ===")
cursor.execute("DESCRIBE notes")
for row in cursor.fetchall():
    print(row)

print("\n=== 檢查 ref 和 ref_time 欄位 ===")
cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'notes'
    AND COLUMN_NAME IN ('ref', 'ref_time')
""")
results = cursor.fetchall()
if results:
    for row in results:
        print(f"✅ {row}")
else:
    print("❌ ref 和 ref_time 欄位不存在")

cursor.close()
conn.close()
