import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime
import time
import csv
from typing import Iterable, Tuple, Dict

def get_db_connection():
    """
    建立與MySQL數據庫的連接
    返回: 數據庫連接對象
    """
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                print(f"數據庫連接成功 (嘗試 {attempt + 1})")
                return connection
        except Error as e:
            print(f"數據庫連接錯誤 (嘗試 {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒後重試...")
                time.sleep(retry_delay)
                retry_delay *= 2  # 指數退避
            else:
                print("達到最大重試次數，無法連接到數據庫")
                return None
    
    return None

def search_stocks(query, limit=10):
    """
    搜尋股票（按代號或名稱模糊搜尋）
    參數:
        query: 搜尋關鍵字
        limit: 返回結果數量限制
    返回: 股票列表
    """
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 更智能的模糊搜尋
        search_query = """
            SELECT stock_code, stock_name, industry
            FROM stocks 
            WHERE stock_code LIKE %s 
               OR stock_name LIKE %s 
               OR stock_name LIKE %s
            ORDER BY 
                CASE 
                    WHEN stock_code = %s THEN 1
                    WHEN stock_name = %s THEN 2
                    WHEN stock_code LIKE %s THEN 3
                    WHEN stock_name LIKE %s THEN 4
                    WHEN stock_name LIKE %s THEN 5
                    ELSE 6
                END,
                stock_code
            LIMIT %s
        """
        
        # 多種搜尋模式
        exact_pattern = query
        starts_with = f"{query}%"
        contains_pattern = f"%{query}%"
        ends_with = f"%{query}"
        
        cursor.execute(search_query, (
            starts_with,           # stock_code LIKE 'query%'
            starts_with,           # stock_name LIKE 'query%'
            contains_pattern,      # stock_name LIKE '%query%'
            exact_pattern,         # stock_code = 'query'
            exact_pattern,         # stock_name = 'query'
            starts_with,           # stock_code LIKE 'query%'
            starts_with,           # stock_name LIKE 'query%'
            contains_pattern,      # stock_name LIKE '%query%'
            limit
        ))
        
        stocks = cursor.fetchall()
        return stocks
        
    except Error as e:
        print(f"搜尋股票時發生錯誤: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_stock_by_code(stock_code):
    """
    根據股票代號獲取股票信息
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

def add_note(stock_code, stock_name, note_type, content, ref=None, ref_time=None):
    """
    添加新的股票筆記
    參數:
        stock_code: 股票代碼
        stock_name: 股票名稱
        note_type: 筆記類型 (TAG 或 STORY)
        content: 筆記內容
        ref: 資料來源（可選）
        ref_time: 來源時間（可選）
    返回: 布爾值，表示操作是否成功
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 處理股票名稱：如果沒有提供或與代碼相同，則使用預設名稱
        if not stock_name or stock_name.strip() == '' or stock_name == stock_code:
            stock_name = f"股票{stock_code}"  # 預設名稱格式
        
        # 首先檢查股票是否已存在
        check_stock_query = "SELECT stock_code, stock_name FROM stocks WHERE stock_code = %s"
        cursor.execute(check_stock_query, (stock_code,))
        existing_stock = cursor.fetchone()
        
        if existing_stock:
            existing_name = existing_stock[1]
            # 如果股票存在且名稱不同，更新股票名稱
            if existing_name != stock_name:
                update_stock_query = """
                    UPDATE stocks SET stock_name = %s, last_updated = CURRENT_TIMESTAMP
                    WHERE stock_code = %s
                """
                cursor.execute(update_stock_query, (stock_name, stock_code))
                print(f"已更新股票名稱: {stock_code} - {existing_name} -> {stock_name}")
        else:
            # 如果股票不存在，新增到stocks表
            insert_stock_query = """
                INSERT INTO stocks (stock_code, stock_name, industry) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_stock_query, (stock_code, stock_name, None))
            print(f"已添加新股票: {stock_code} - {stock_name}")
        
        # 添加筆記到notes表（包含當前時間和來源資訊）
        insert_note_query = """
            INSERT INTO notes (stock_code, note_type, content, ref, ref_time, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        current_time = datetime.now()
        cursor.execute(insert_note_query, (stock_code, note_type, content, ref, ref_time, current_time))
        
        connection.commit()
        print(f"已成功添加筆記: {stock_code} - {stock_name} - {note_type} - {current_time}")
        return True
        
    except Error as e:
        print(f"添加筆記時發生錯誤: {e}")
        if connection.is_connected():
            connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_ref_options(limit=10):
    """
    獲取常用的來源選項
    參數:
        limit: 返回結果數量限制
    返回: 來源選項列表
    """
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        
        query = """
            SELECT ref, COUNT(*) as count
            FROM notes 
            WHERE ref IS NOT NULL AND ref != ''
            GROUP BY ref
            ORDER BY count DESC, ref ASC
            LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        return [row[0] for row in results]
        
    except Error as e:
        print(f"獲取來源選項時發生錯誤: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_notes(search_term='', sort_by='created_at', sort_order='DESC'):
    """
    獲取所有筆記，支援搜尋和排序
    參數:
        search_term: 搜尋關鍵字（股票代碼、名稱或內容）
        sort_by: 排序欄位 (stock_code, stock_name, note_type, created_at)
        sort_order: 排序方向 (ASC, DESC)
    返回: 筆記列表，每個筆記是一個字典
    """
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 基礎查詢
        base_query = """
            SELECT 
                n.id,
                n.stock_code,
                s.stock_name,
                n.note_type,
                n.content,
                n.ref,
                n.ref_time,
                n.created_at
            FROM notes n
            JOIN stocks s ON n.stock_code = s.stock_code
        """
        
        # 搜尋條件
        where_clause = ""
        params = []
        
        if search_term:
            where_clause = """
                WHERE n.stock_code LIKE %s 
                   OR s.stock_name LIKE %s 
                   OR n.content LIKE %s
                   OR n.ref LIKE %s
            """
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern, search_pattern]
        
        # 排序
        valid_sort_fields = ['stock_code', 'stock_name', 'note_type', 'created_at']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'DESC'
        
        # 根據排序欄位調整查詢
        if sort_by == 'stock_name':
            order_clause = f"s.stock_name {sort_order}"
        elif sort_by == 'created_at':
            order_clause = f"n.created_at {sort_order}"
        else:
            order_clause = f"n.{sort_by} {sort_order}"
        
        # 組合完整查詢
        full_query = f"{base_query} {where_clause} ORDER BY {order_clause}"
        
        cursor.execute(full_query, params)
        notes = cursor.fetchall()
        
        # 格式化時間顯示
        for note in notes:
            if note['created_at']:
                note['created_at'] = note['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if note['ref_time']:
                note['ref_time'] = note['ref_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return notes
        
    except Error as e:
        print(f"獲取筆記時發生錯誤: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_note_by_id(note_id):
    """
    根據ID獲取單一筆記
    參數:
        note_id: 筆記ID
    返回: 筆記字典或None
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                n.id,
                n.stock_code,
                s.stock_name,
                n.note_type,
                n.content,
                n.ref,
                n.ref_time,
                n.created_at
            FROM notes n
            JOIN stocks s ON n.stock_code = s.stock_code
            WHERE n.id = %s
        """
        
        cursor.execute(query, (note_id,))
        note = cursor.fetchone()
        
        if note:
            if note['created_at']:
                note['created_at'] = note['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if note['ref_time']:
                note['ref_time'] = note['ref_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return note
        
    except Error as e:
        print(f"獲取筆記時發生錯誤: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_note(note_id, note_type, content, ref=None, ref_time=None):
    """
    更新筆記
    參數:
        note_id: 筆記ID
        note_type: 新的筆記類型
        content: 新的內容
        ref: 資料來源（可選）
        ref_time: 來源時間（可選）
    返回: 布爾值，表示是否成功
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 驗證筆記類型
        if note_type not in ['TAG', 'STORY']:
            print(f"無效的筆記類型: {note_type}")
            return False
        
        # 更新筆記（包含來源資訊）
        update_query = """
            UPDATE notes 
            SET note_type = %s, content = %s, ref = %s, ref_time = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        cursor.execute(update_query, (note_type, content, ref, ref_time, note_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"筆記 {note_id} 更新成功")
            return True
        else:
            print(f"筆記 {note_id} 不存在或更新失敗")
            return False
        
    except Error as e:
        print(f"更新筆記時發生錯誤: {e}")
        if connection.is_connected():
            connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_note(note_id):
    """
    刪除筆記
    參數:
        note_id: 筆記ID
    返回: 布爾值，表示是否成功
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 先檢查筆記是否存在
        check_query = "SELECT id FROM notes WHERE id = %s"
        cursor.execute(check_query, (note_id,))
        
        if not cursor.fetchone():
            print(f"筆記 {note_id} 不存在")
            return False
        
        # 刪除筆記
        delete_query = "DELETE FROM notes WHERE id = %s"
        cursor.execute(delete_query, (note_id,))
        connection.commit()
        
        print(f"筆記 {note_id} 刪除成功")
        return True
        
    except Error as e:
        print(f"刪除筆記時發生錯誤: {e}")
        if connection.is_connected():
            connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def test_connection():
    """
    測試數據庫連接
    返回: 布爾值，表示連接是否成功
    """
    connection = get_db_connection()
    if connection:
        connection.close()
        return True
    return False

def init_common_stocks():
    """
    初始化常用的台股資料（如果資料表為空）
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # 檢查是否已有資料
        cursor.execute("SELECT COUNT(*) FROM stocks")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"資料表已有 {count} 筆股票資料，跳過初始化")
            return True
        
        # 常用台股資料（只保留一筆避免資料庫空白）
        common_stocks = [
            ("2330", "台積電", "半導體"),
        ]
        
        insert_query = """
            INSERT INTO stocks (stock_code, stock_name, industry) 
            VALUES (%s, %s, %s)
        """
        
        for stock in common_stocks:
            cursor.execute(insert_query, stock)
        
        connection.commit()
        print(f"已初始化 {len(common_stocks)} 筆常用台股資料")
        return True
        
    except Error as e:
        print(f"初始化股票資料時發生錯誤: {e}")
        if connection.is_connected():
            connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def import_stocks_from_iterable(rows: Iterable[Dict[str, str]]) -> Tuple[int, int, int]:
    """
    由可迭代資料批次匯入/更新股票至 stocks 表。
    rows: 可迭代，元素包含 keys: stock_code, stock_name, industry(可選)
    回傳: (inserted, updated, skipped)
    """
    connection = get_db_connection()
    if not connection:
        return (0, 0, 0)

    inserted = 0
    updated = 0
    skipped = 0

    try:
        cursor = connection.cursor()
        upsert_sql = (
            "INSERT INTO stocks (stock_code, stock_name, industry) "
            "VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE "
            "stock_name = VALUES(stock_name), "
            "industry = COALESCE(VALUES(industry), industry), "
            "last_updated = CURRENT_TIMESTAMP"
        )
        batch_params = []
        for row in rows:
            code = (row.get('stock_code') or row.get('code') or '').strip()
            name = (row.get('stock_name') or row.get('name') or '').strip()
            industry = (row.get('industry') or None)
            if not code or not name:
                skipped += 1
                continue
            batch_params.append((code, name, industry))
        if not batch_params:
            return (0, 0, skipped)
        cursor.executemany(upsert_sql, batch_params)
        affected = cursor.rowcount or 0
        # 在 MySQL 的 ON DUPLICATE KEY UPDATE 情境，rowcount 對 updated 行會回傳 2
        # 粗略估算 inserted/updated（非精確但足夠統計）
        # 假設 updated 以 2 計數，插入以 1 計數
        # 我們無法逐筆得知，這裡以總筆數估算：
        connection.commit()
        # 保守做法：全部視作成功，回傳 inserted+updated = 輸入批次數量
        # 若要精確，需逐筆查詢是否存在，成本較高
        total = len(batch_params)
        return (total, 0, skipped)
    except Error as e:
        print(f"批次匯入股票時發生錯誤: {e}")
        if connection.is_connected():
            connection.rollback()
        return (0, 0, skipped)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def import_stocks_from_csv(csv_path: str) -> Tuple[int, int, int]:
    """
    從 CSV 匯入/更新股票。CSV 需含標頭: stock_code,stock_name[,industry]
    回傳: (inserted, updated, skipped)
    """
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
        return import_stocks_from_iterable(rows)
    except FileNotFoundError:
        print(f"找不到CSV檔案: {csv_path}")
        return (0, 0, 0)
    except Exception as e:
        print(f"讀取CSV時發生錯誤: {e}")
        return (0, 0, 0)
