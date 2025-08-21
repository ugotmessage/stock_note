from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import db_manager
import external_api

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/', methods=['GET'])
def index():
	try:
		notes = db_manager.get_all_notes()
		return render_template('index.html', notes=notes)
	except Exception as e:
		print(f"主頁加載錯誤: {e}")
		flash('加載數據時發生錯誤', 'error')
		return render_template('index.html', notes=[])


@app.route('/search-stocks', methods=['GET'])
def search_stocks():
	"""優先從本地 DB 模糊搜尋，若無結果再退回 Yahoo Finance API 提供即時搜尋建議"""
	try:
		query = request.args.get('q', '').strip()
		print(f"收到搜尋請求: '{query}'")
		
		if not query:
			print("查詢為空，返回空結果")
			return jsonify([])

		results = []

		# 1) 先從本地 stocks 資料表模糊查詢
		print("嘗試本地搜尋...")
		locals_ = db_manager.search_stocks(query, limit=10)
		print(f"本地搜尋返回 {len(locals_)} 個結果")
		
		for s in locals_:
			results.append({
				'code': s['stock_code'],
				'name': s['stock_name'],
				'display': f"{s['stock_code']} - {s['stock_name']}"
			})

		# 2) 若本地無結果，再呼叫 Yahoo Finance 搜尋
		if not results:
			print("本地無結果，呼叫 Yahoo Finance API...")
			externals = external_api.search_yahoo_stocks(query, limit=10)
			print(f"Yahoo API 返回 {len(externals)} 個結果")
			
			for s in externals:
				# 為了避免重複，再次確認代碼是否已存在 (雖然理論上此時 results 應為空)
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

		if not stock_code:
			flash('請輸入股票代碼', 'error')
			return redirect(url_for('index'))
		if not stock_name:
			flash('請輸入或選擇股票名稱', 'error')
			return redirect(url_for('index'))
		if note_type not in ['TAG', 'STORY']:
			flash('無效的筆記類型', 'error')
			return redirect(url_for('index'))
		if not content:
			flash('請輸入筆記內容', 'error')
			return redirect(url_for('index'))

		success = db_manager.add_note(stock_code, stock_name, note_type, content)
		flash(('成功添加筆記: ' if success else '添加筆記失敗，請稍後重試') + f'{stock_code} - {stock_name}', 'success' if success else 'error')
	except Exception as e:
		print(f"添加筆記時發生錯誤: {e}")
		flash('系統錯誤，請稍後重試', 'error')
	return redirect(url_for('index'))


@app.route('/admin/import-stocks', methods=['POST'])
def admin_import_stocks():
	"""從伺服器 data/example_stocks.csv 匯入/更新股票資料"""
	csv_path = request.form.get('csv_path', 'data/example_stocks.csv').strip()
	inserted, updated, skipped = db_manager.import_stocks_from_csv(csv_path)
	flash(f'匯入完成: 成功 {inserted} 筆, 略過 {skipped} 筆（ CSV: {csv_path} ）', 'success')
	return redirect(url_for('index'))


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
	
	# 測試數據庫連接
	print("測試數據庫連接...")
	if db_manager.test_connection():
		print("✅ 數據庫連接成功")
		
		# 初始化常用股票資料
		print("初始化常用股票資料...")
		if db_manager.init_common_stocks():
			print("✅ 股票資料初始化完成")
		else:
			print("❌ 股票資料初始化失敗")
	else:
		print("❌ 數據庫連接失敗")
	
	# 在開發環境中啟用調試模式
	debug_mode = os.getenv('FLASK_ENV') == 'development'
	app.run(debug=debug_mode, host='0.0.0.0', port=5000)
