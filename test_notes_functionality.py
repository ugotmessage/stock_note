#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票筆記管理系統功能測試腳本
測試搜尋、排序、編輯和刪除功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import db_manager
from datetime import datetime

def test_notes_functionality():
    """測試筆記相關功能"""
    print("🧪 開始測試筆記管理功能...\n")
    
    # 測試 1: 連接資料庫
    print("1. 測試資料庫連接...")
    if not db_manager.test_connection():
        print("❌ 資料庫連接失敗")
        return False
    print("✅ 資料庫連接成功\n")
    
    # 測試 2: 添加測試筆記
    print("2. 測試添加筆記...")
    test_notes = [
        ("2330", "台積電", "TAG", "測試標籤：護國神山"),
        ("2317", "鴻海", "STORY", "測試故事：代工龍頭的故事"),
        ("2454", "聯發科", "TAG", "測試標籤：手機晶片大廠"),
        ("2412", "中華電", "STORY", "測試故事：電信業龍頭"),
    ]
    
    for stock_code, stock_name, note_type, content in test_notes:
        success = db_manager.add_note(stock_code, stock_name, note_type, content)
        if success:
            print(f"✅ 添加筆記成功: {stock_code} - {note_type}")
        else:
            print(f"❌ 添加筆記失敗: {stock_code} - {note_type}")
    print()
    
    # 測試 3: 測試搜尋功能
    print("3. 測試搜尋功能...")
    search_tests = [
        ("台積電", "按股票名稱搜尋"),
        ("TAG", "按筆記類型搜尋"),
        ("護國神山", "按內容搜尋"),
        ("2330", "按股票代碼搜尋"),
    ]
    
    for query, description in search_tests:
        notes = db_manager.get_all_notes(search_term=query)
        print(f"🔍 {description} '{query}': 找到 {len(notes)} 條筆記")
        for note in notes[:2]:  # 只顯示前2條
            print(f"   - {note['stock_code']} {note['stock_name']}: {note['content'][:30]}...")
    print()
    
    # 測試 4: 測試排序功能
    print("4. 測試排序功能...")
    sort_tests = [
        ("stock_code", "ASC", "按股票代碼升序"),
        ("stock_code", "DESC", "按股票代碼降序"),
        ("created_at", "DESC", "按創建時間降序"),
        ("note_type", "ASC", "按筆記類型升序"),
    ]
    
    for sort_by, sort_order, description in sort_tests:
        notes = db_manager.get_all_notes(sort_by=sort_by, sort_order=sort_order)
        print(f"📊 {description}: 前3條")
        for i, note in enumerate(notes[:3]):
            print(f"   {i+1}. {note['stock_code']} {note['stock_name']} ({note['note_type']})")
    print()
    
    # 測試 5: 測試獲取單一筆記
    print("5. 測試獲取單一筆記...")
    all_notes = db_manager.get_all_notes()
    if all_notes:
        first_note = all_notes[0]
        note_id = first_note['id']
        note = db_manager.get_note_by_id(note_id)
        if note:
            print(f"✅ 成功獲取筆記 ID {note_id}: {note['stock_code']} - {note['content'][:30]}...")
        else:
            print(f"❌ 獲取筆記 ID {note_id} 失敗")
    print()
    
    # 測試 6: 測試更新筆記
    print("6. 測試更新筆記...")
    if all_notes:
        first_note = all_notes[0]
        note_id = first_note['id']
        new_content = f"更新後的內容 - {datetime.now().strftime('%H:%M:%S')}"
        
        success = db_manager.update_note(note_id, "STORY", new_content)
        if success:
            print(f"✅ 筆記更新成功: {new_content}")
            
            # 驗證更新
            updated_note = db_manager.get_note_by_id(note_id)
            if updated_note and updated_note['content'] == new_content:
                print(f"✅ 更新驗證成功")
            else:
                print(f"❌ 更新驗證失敗")
        else:
            print(f"❌ 筆記更新失敗")
    print()
    
    # 測試 7: 測試刪除筆記
    print("7. 測試刪除筆記...")
    if all_notes:
        last_note = all_notes[-1]
        note_id = last_note['id']
        
        success = db_manager.delete_note(note_id)
        if success:
            print(f"✅ 筆記刪除成功: ID {note_id}")
            
            # 驗證刪除
            deleted_note = db_manager.get_note_by_id(note_id)
            if deleted_note is None:
                print(f"✅ 刪除驗證成功")
            else:
                print(f"❌ 刪除驗證失敗")
        else:
            print(f"❌ 筆記刪除失敗")
    print()
    
    # 測試 8: 最終統計
    print("8. 最終統計...")
    final_notes = db_manager.get_all_notes()
    print(f"📊 目前共有 {len(final_notes)} 條筆記")
    
    if final_notes:
        print("📋 筆記列表:")
        for note in final_notes:
            print(f"   - {note['stock_code']} {note['stock_name']}: {note['note_type']} - {note['content'][:40]}...")
    
    print("\n🎉 所有測試完成！")
    return True

if __name__ == "__main__":
    try:
        test_notes_functionality()
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
