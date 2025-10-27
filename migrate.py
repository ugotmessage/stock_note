#!/usr/bin/env python3
"""
資料庫遷移管理腳本
用於執行資料庫結構變更和版本控制
"""

import os
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import glob
import re
from datetime import datetime

def get_db_connection():
    """建立資料庫連接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"資料庫連接錯誤: {e}")
        return None

def create_migration_table():
    """創建遷移記錄表"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        print("✅ 遷移記錄表已創建或已存在")
        return True
        
    except Error as e:
        print(f"❌ 創建遷移記錄表失敗: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_executed_migrations():
    """獲取已執行的遷移列表"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT migration_name FROM migrations ORDER BY id")
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Error as e:
        print(f"❌ 獲取已執行遷移失敗: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute_migration(migration_file):
    """執行單個遷移文件"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 讀取遷移文件
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割 SQL 語句（以分號分隔）
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        # 執行每個 SQL 語句
        for statement in sql_statements:
            if statement:
                cursor.execute(statement)
        
        # 記錄遷移執行
        migration_name = os.path.basename(migration_file)
        description = extract_description(sql_content)
        
        insert_migration_sql = """
        INSERT INTO migrations (migration_name, description) 
        VALUES (%s, %s)
        """
        cursor.execute(insert_migration_sql, (migration_name, description))
        
        connection.commit()
        print(f"✅ 遷移執行成功: {migration_name}")
        return True
        
    except Error as e:
        print(f"❌ 遷移執行失敗 {migration_file}: {e}")
        if connection.is_connected():
            connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def extract_description(sql_content):
    """從 SQL 內容中提取描述"""
    lines = sql_content.split('\n')
    for line in lines:
        if '-- 描述:' in line:
            return line.split('-- 描述:')[1].strip()
    return "無描述"

def run_migrations():
    """執行所有未執行的遷移"""
    print("🚀 開始執行資料庫遷移...")
    
    # 創建遷移記錄表
    if not create_migration_table():
        return False
    
    # 獲取已執行的遷移
    executed_migrations = get_executed_migrations()
    print(f"📋 已執行的遷移: {executed_migrations}")
    
    # 獲取所有遷移文件
    migration_files = sorted(glob.glob("migrations/*.sql"))
    
    if not migration_files:
        print("⚠️  沒有找到遷移文件")
        return True
    
    print(f"📁 找到 {len(migration_files)} 個遷移文件")
    
    success_count = 0
    for migration_file in migration_files:
        migration_name = os.path.basename(migration_file)
        
        if migration_name in executed_migrations:
            print(f"⏭️  跳過已執行的遷移: {migration_name}")
            continue
        
        print(f"🔄 執行遷移: {migration_name}")
        if execute_migration(migration_file):
            success_count += 1
        else:
            print(f"❌ 遷移失敗，停止執行: {migration_name}")
            return False
    
    print(f"✅ 遷移完成！成功執行 {success_count} 個遷移")
    return True

def show_status():
    """顯示遷移狀態"""
    print("📊 遷移狀態:")
    
    executed_migrations = get_executed_migrations()
    migration_files = sorted(glob.glob("migrations/*.sql"))
    
    print(f"已執行: {len(executed_migrations)} 個")
    print(f"總計: {len(migration_files)} 個")
    
    for migration_file in migration_files:
        migration_name = os.path.basename(migration_file)
        status = "✅ 已執行" if migration_name in executed_migrations else "⏳ 待執行"
        print(f"  {migration_name}: {status}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "status":
            show_status()
        elif command == "migrate":
            run_migrations()
        else:
            print("用法: python migrate.py [status|migrate]")
    else:
        run_migrations()

