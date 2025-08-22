from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import db_manager
import external_api

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/', methods=['GET'])
def index():
    try:
        # 從 URL 獲取搜尋和排序參數
        search_term = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'DESC')

        # 呼叫更新後的函式
        notes = db_manager.get_all_notes(search_term, sort_by, sort_order)
        
        # 將參數傳給模板，以便在介面上顯示當前狀態
        return render_template('index.html', 
                               notes=notes, 
                               search_term=search_term,
                               sort_by=sort_by,
                               sort_order=sort_order)
    except Exception as e:
        print(f"主頁加載錯誤: {e}")
        flash('加載數據時發生錯誤', 'error')
        return render_template('index.html', notes=[])

# --- 新增 API 路由 ---

@app.route('/api/notes', methods=['GET'])
def api_get_notes():
    """API 路由：獲取筆記列表（支援搜尋和排序）"""
    try:
        search_term = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'DESC')

        notes = db_manager.get_all_notes(search_term, sort_by, sort_order)
        
        return jsonify({
            'success': True,
            'notes': notes,
            'total': len(notes),
            'search_term': search_term,
            'sort_by': sort_by,
            'sort_order': sort_order
        })
    except Exception as e:
        print(f"API 獲取筆記錯誤: {e}")
        return jsonify({
            'success': False,
            'error': '獲取筆記時發生錯誤',
            'message': str(e)
        }), 500

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def api_get_note(note_id):
    """API 路由：獲取單一筆記"""
    try:
        note = db_manager.get_note_by_id(note_id)
        
        if note:
            return jsonify({
                'success': True,
                'note': note
            })
        else:
            return jsonify({
                'success': False,
                'error': '找不到該筆記'
            }), 404
    except Exception as e:
        print(f"API 獲取筆記錯誤: {e}")
        return jsonify({
            'success': False,
            'error': '獲取筆記時發生錯誤',
            'message': str(e)
        }), 500

# --- 修改現有的編輯和刪除路由，支援 JSON 回應 ---

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'POST':
        note_type = request.form.get('note_type', '').strip()
        content = request.form.get('content', '').strip()

        if note_type not in ['TAG', 'STORY'] or not content:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'error': '筆記類型或內容無效'}), 400
            flash('筆記類型或內容無效', 'error')
            return redirect(url_for('edit_note', note_id=note_id))

        success = db_manager.update_note(note_id, note_type, content)
        if success:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': True, 'message': '筆記更新成功'})
            flash('筆記更新成功', 'success')
            return redirect(url_for('index'))
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'success': False, 'error': '筆記更新失敗'}), 500
            flash('筆記更新失敗', 'error')
            
    # 處理 GET 請求
    note = db_manager.get_note_by_id(note_id)
    if not note:
        flash('找不到該筆記', 'error')
        return redirect(url_for('index'))
        
    # 根據筆記中的 stock_code 獲取股票完整資訊
    stock_info = db_manager.get_stock_by_code(note['stock_code'])
    return render_template('edit_note.html', note=note, stock_info=stock_info)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note_route(note_id):
    success = db_manager.delete_note(note_id)
    
    if request.headers.get('Content-Type') == 'application/json':
        if success:
            return jsonify({'success': True, 'message': '筆記已刪除'})
        else:
            return jsonify({'success': False, 'error': '刪除失敗'}), 500
    
    if success:
        flash('筆記已刪除', 'success')
    else:
        flash('刪除失敗', 'error')
    return redirect(url_for('index'))

# --- 其他路由維持不變 ---

@app.route('/search-stocks', methods=['GET'])
def search_stocks():
    """優先從本地 DB 模糊搜尋，若無結果再退回 Yahoo Finance API"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])

        results = []
        
        print("嘗試本地搜尋...")
        locals_ = db_manager.search_stocks(query, limit=10)
        print(f"本地搜尋返回 {len(locals_)} 個結果")
        
        for s in locals_:
            results.append({
                'code': s['stock_code'],
                'name': s['stock_name'],
                'display': f"{s['stock_code']} - {s['stock_name']}"
            })

        if not results:
            print("本地無結果，呼叫 Yahoo Finance API...")
            externals = external_api.search_yahoo_stocks(query, limit=10)
            print(f"Yahoo API 返回 {len(externals)} 個結果")
            
            for s in externals:
                if not any(r['code'] == s['code'] for r in results):
                    results.append({
                        'code': s['code'],
                        'name': s['name'],
                        'display': f"{s['code']} - {s['name']}"
                    })

        print(f"最終返回 {len(results)} 個結果")
        return jsonify(results)
        
    except Exception as e:
        print(f"股票搜尋錯誤: {e}")
        import traceback
        traceback.print_exc()
        return jsonify([])

@app.route('/get-stock-info', methods=['GET'])
def get_stock_info():
	try:
		stock_code = request.args.get('code', '').strip()
		if not stock_code:
			return jsonify({'error': '股票代號不能為空'})

		stock = db_manager.get_stock_by_code(stock_code)
		if stock:
			return jsonify({'code': stock['stock_code'], 'name': stock['stock_name'], 'industry': stock.get('industry', '')})
		return jsonify({'error': '找不到該股票'})
	except Exception as e:
		print(f"獲取股票信息錯誤: {e}")
		return jsonify({'error': '系統錯誤'})


@app.route('/add', methods=['POST'])
def add_note():
	try:
		stock_code = request.form.get('stock_code', '').strip()
		stock_name = request.form.get('stock_name', '').strip()
		note_type = request.form.get('note_type', '').strip()
		content = request.form.get('content', '').strip()

		if not all([stock_code, stock_name, note_type, content]):
			flash('所有欄位都是必填的', 'error')
			return redirect(url_for('index'))
		if note_type not in ['TAG', 'STORY']:
			flash('無效的筆記類型', 'error')
			return redirect(url_for('index'))

		success = db_manager.add_note(stock_code, stock_name, note_type, content)
		flash(f'成功添加筆記: {stock_code} - {stock_name}', 'success' if success else '添加筆記失敗', 'error')
	except Exception as e:
		print(f"添加筆記時發生錯誤: {e}")
		flash('系統錯誤，請稍後重試', 'error')
	return redirect(url_for('index'))

# ... (health_check, test_database 等函式維持不變) ...
@app.route('/health')
def health_check():
	try:
		db_status = 'connected' if db_manager.test_connection() else 'disconnected'
		return {'status': 'healthy', 'message': '股票筆記管理系統運行正常', 'database': db_status, 'environment': os.getenv('FLASK_ENV', 'production')}
	except Exception as e:
		return {'status': 'unhealthy', 'message': f'系統錯誤: {str(e)}', 'database': 'unknown'}


@app.route('/test-db')
def test_database():
	try:
		return {'status': 'success', 'message': '數據庫連接正常'} if db_manager.test_connection() else {'status': 'error', 'message': '無法連接到數據庫'}
	except Exception as e:
		return {'status': 'error', 'message': f'測試失敗: {str(e)}'}

if __name__ == '__main__':
    print('啟動股票筆記管理系統...')
    if db_manager.test_connection():
        print("✅ 數據庫連接成功")
        if db_manager.init_common_stocks():
            print("✅ 股票資料初始化完成")
        else:
            print("❌ 股票資料初始化失敗")
    else:
        print("❌ 數據庫連接失敗")
    
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)