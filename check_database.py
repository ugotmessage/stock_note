#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查資料庫結構的簡單腳本
"""

import db_manager

def check_database_structure():
    """檢查資料庫結構"""
    print("🔍 檢查資料庫結構...")
    
    # 測試連接
    if not db_manager.test_connection():
        print("❌ 無法連接到資料庫")
        return
    
    print("✅ 資料庫連接成功")
    
    # 檢查 notes 表結構
    try:
        connection = db_manager.get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # 檢查 notes 表欄位
            cursor.execute("DESCRIBE notes")
            columns = cursor.fetchall()
            
            print("\n📋 notes 表結構:")
            print(f"{'欄位名':<15} {'類型':<20} {'NULL':<8} {'KEY':<8} {'預設值':<15} {'額外':<15}")
            print("-" * 80)
            
            has_updated_at = False
            for col in columns:
                print(f"{col[0]:<15} {col[1]:<20} {col[2]:<8} {col[3]:<8} {str(col[4]):<15} {str(col[5]):<15}")
                if col[0] == 'updated_at':
                    has_updated_at = True
            
            if not has_updated_at:
                print("\n⚠️  缺少 updated_at 欄位，建議執行 update_database.sql")
            else:
                print("\n✅ updated_at 欄位已存在")
            
            # 檢查索引
            cursor.execute("SHOW INDEX FROM notes")
            indexes = cursor.fetchall()
            
            print("\n🔗 notes 表索引:")
            for idx in indexes:
                print(f"  - {idx[2]} ({idx[4]})")
            
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"❌ 檢查資料庫結構時發生錯誤: {e}")

if __name__ == "__main__":
    check_database_structure()
