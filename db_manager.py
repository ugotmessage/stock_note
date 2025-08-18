import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime

def get_db_connection():
    """
    建立與MySQL數據庫的連接
    返回: 數據庫連接對象
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"數據庫連接錯誤: {e}")
        return None

def add_note(stock_code, note_type, content):
    """
    添加新的股票筆記
    參數:
        stock_code: 股票代碼
        note_type: 筆記類型 (TAG 或 STORY)
        content: 筆記內容
    返回: 布爾值，表示操作是否成功
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 首先檢查股票是否已存在
        check_stock_query = "SELECT stock_code FROM stocks WHERE stock_code = %s"
        cursor.execute(check_stock_query, (stock_code,))
        stock_exists = cursor.fetchone()
        
        # 如果股票不存在，先添加到stocks表
        if not stock_exists:
            insert_stock_query = """
                INSERT INTO stocks (stock_code, stock_name, industry) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_stock_query, (stock_code, stock_code, None))
            print(f"已添加新股票: {stock_code}")
        
        # 添加筆記到notes表
        insert_note_query = """
            INSERT INTO notes (stock_code, note_type, content) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_note_query, (stock_code, note_type, content))
        
        connection.commit()
        print(f"已成功添加筆記: {stock_code} - {note_type}")
        return True
        
    except Error as e:
        print(f"添加筆記時發生錯誤: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_notes():
    """
    獲取所有筆記，按創建時間倒序排列
    返回: 筆記列表，每個筆記是一個字典
    """
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 查詢所有筆記，並聯接stocks表獲取股票名稱
        query = """
            SELECT 
                n.id,
                n.stock_code,
                s.stock_name,
                n.note_type,
                n.content,
                n.created_at
            FROM notes n
            JOIN stocks s ON n.stock_code = s.stock_code
            ORDER BY n.created_at DESC
        """
        
        cursor.execute(query)
        notes = cursor.fetchall()
        
        # 格式化時間顯示
        for note in notes:
            if note['created_at']:
                note['created_at'] = note['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return notes
        
    except Error as e:
        print(f"獲取筆記時發生錯誤: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_stock_info(stock_code):
    """
    獲取特定股票的信息
    參數: stock_code - 股票代碼
    返回: 股票信息字典
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM stocks WHERE stock_code = %s"
        cursor.execute(query, (stock_code,))
        stock = cursor.fetchone()
        
        return stock
        
    except Error as e:
        print(f"獲取股票信息時發生錯誤: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
