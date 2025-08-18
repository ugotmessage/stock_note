from flask import Flask, render_template, request, redirect, url_for, flash
import db_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用於flash消息

@app.route('/', methods=['GET'])
def index():
    """
    主頁路由 - 顯示所有筆記和添加筆記的表單
    """
    try:
        # 獲取所有筆記數據
        notes = db_manager.get_all_notes()
        return render_template('index.html', notes=notes)
    except Exception as e:
        print(f"主頁加載錯誤: {e}")
        flash('加載數據時發生錯誤', 'error')
        return render_template('index.html', notes=[])

@app.route('/add', methods=['POST'])
def add_note():
    """
    添加筆記的路由 - 處理表單提交
    """
    try:
        # 獲取表單數據
        stock_code = request.form.get('stock_code', '').strip()
        note_type = request.form.get('note_type', '').strip()
        content = request.form.get('content', '').strip()
        
        # 基本驗證
        if not stock_code:
            flash('請輸入股票代碼', 'error')
            return redirect(url_for('index'))
        
        if not note_type:
            flash('請選擇筆記類型', 'error')
            return redirect(url_for('index'))
        
        if not content:
            flash('請輸入筆記內容', 'error')
            return redirect(url_for('index'))
        
        # 驗證note_type是否為有效值
        if note_type not in ['TAG', 'STORY']:
            flash('無效的筆記類型', 'error')
            return redirect(url_for('index'))
        
        # 調用數據庫管理器添加筆記
        success = db_manager.add_note(stock_code, note_type, content)
        
        if success:
            flash(f'成功添加筆記: {stock_code}', 'success')
        else:
            flash('添加筆記失敗，請稍後重試', 'error')
            
    except Exception as e:
        print(f"添加筆記時發生錯誤: {e}")
        flash('系統錯誤，請稍後重試', 'error')
    
    # 重定向回主頁
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """
    健康檢查端點
    """
    return {'status': 'healthy', 'message': '股票筆記管理系統運行正常'}

if __name__ == '__main__':
    print("啟動股票筆記管理系統...")
    print("請確保MySQL數據庫已啟動且配置正確")
    print("訪問 http://localhost:5000 查看系統")
    
    # 在開發環境中啟用調試模式
    app.run(debug=True, host='0.0.0.0', port=5000)
