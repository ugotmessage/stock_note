#!/usr/bin/env python3
"""
驗證遷移狀態和數據庫結構
"""

import mysql.connector
from config import DB_CONFIG

def check_migration_status():
    """檢查遷移記錄"""
    print("=" * 50)
    print("📊 遷移記錄狀態")
    print("=" * 50)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("SELECT migration_name, executed_at FROM migrations ORDER BY executed_at")
    migrations = cursor.fetchall()
    
    if migrations:
        print(f"✅ 已執行 {len(migrations)} 個遷移:")
        for name, executed_at in migrations:
            print(f"  - {name} (於 {executed_at})")
    else:
        print("⚠️  沒有遷移記錄")
    
    cursor.close()
    conn.close()

def check_table_structure():
    """檢查表結構"""
    print("\n" + "=" * 50)
    print("📋 notes 表結構")
    print("=" * 50)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("DESCRIBE notes")
    columns = cursor.fetchall()
    
    print(f"\n總共有 {len(columns)} 個欄位:")
    for i, col in enumerate(columns, 1):
        col_name, col_type, null, key, default, extra = col
        print(f"\n{i}. {col_name}")
        print(f"   類型: {col_type}")
        print(f"   可為空: {null}")
        print(f"   索引: {key}")
    
    cursor.close()
    conn.close()

def check_specific_columns():
    """檢查特定欄位"""
    print("\n" + "=" * 50)
    print("🔍 檢查來源欄位")
    print("=" * 50)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 檢查 ref 和 ref_time
    target_columns = ['ref', 'ref_time']
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_COMMENT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'notes'
        AND COLUMN_NAME IN ('ref', 'ref_time')
    """)
    
    results = cursor.fetchall()
    found_columns = {row[0]: row for row in results}
    
    for col_name in target_columns:
        if col_name in found_columns:
            _, data_type, is_null, comment = found_columns[col_name]
            print(f"✅ {col_name}")
            print(f"   類型: {data_type}")
            print(f"   可為空: {is_null}")
            print(f"   註釋: {comment or '無'}")
        else:
            print(f"❌ {col_name} - 欄位不存在！")
    
    cursor.close()
    conn.close()

def check_indexes():
    """檢查索引"""
    print("\n" + "=" * 50)
    print("📑 檢查索引")
    print("=" * 50)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("SHOW INDEX FROM notes")
    indexes = cursor.fetchall()
    
    index_names = {}
    for row in indexes:
        key_name = row[2]
        column_name = row[4]
        if key_name not in index_names:
            index_names[key_name] = []
        index_names[key_name].append(column_name)
    
    print(f"\n總共有 {len(index_names)} 個索引:")
    for key_name, columns in sorted(index_names.items()):
        print(f"  - {key_name}: {', '.join(columns)}")
    
    # 檢查特定索引
    target_indexes = ['idx_notes_ref', 'idx_notes_ref_time']
    print("\n檢查來源相關索引:")
    for idx_name in target_indexes:
        if idx_name in index_names:
            print(f"  ✅ {idx_name}")
        else:
            print(f"  ❌ {idx_name} - 索引不存在")
    
    cursor.close()
    conn.close()

def summary():
    """總結"""
    print("\n" + "=" * 50)
    print("📊 驗證總結")
    print("=" * 50)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 檢查關鍵欄位
    cursor.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'notes'
        AND COLUMN_NAME IN ('id', 'stock_code', 'note_type', 'content', 
                           'created_at', 'updated_at', 'ref', 'ref_time')
    """)
    
    columns = [row[0] for row in cursor.fetchall()]
    required_columns = ['id', 'stock_code', 'note_type', 'content', 
                       'created_at', 'updated_at', 'ref', 'ref_time']
    
    print("\n必需的欄位:")
    for col in required_columns:
        if col in columns:
            print(f"  ✅ {col}")
        else:
            print(f"  ❌ {col} - 缺失！")
    
    # 檢查數據
    cursor.execute("SELECT COUNT(*) FROM notes")
    note_count = cursor.fetchone()[0]
    print(f"\n📝 筆記數量: {note_count} 條")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        check_migration_status()
        check_table_structure()
        check_specific_columns()
        check_indexes()
        summary()
        print("\n🎉 驗證完成！")
    except Exception as e:
        print(f"\n❌ 驗證失敗: {e}")
        import traceback
        traceback.print_exc()

