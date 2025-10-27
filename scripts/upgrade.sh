#!/bin/bash

# 版本升級腳本
# 用於從舊版本升級到新版本

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_step() {
    echo -e "${MAGENTA}► ${NC}$1"
}

# 顯示版本升級提示
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    股票筆記系統 - 版本升級腳本            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# 檢查是否在正確的目錄
if [ ! -f "app.py" ]; then
    print_error "請在專案根目錄執行此腳本"
    exit 1
fi

# 函數：檢查是否使用 Docker
check_docker() {
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        if [ -f "docker-compose.yml" ] || [ -f "docker-compose.standalone.yml" ]; then
            return 0
        fi
    fi
    return 1
}

# 函數：備份數據庫
backup_database() {
    print_step "步驟 1: 備份數據庫"
    
    if check_docker; then
        # Docker 環境
        CONTAINER_NAME="stock-note-app"
        
        if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
            print_info "使用 Docker 備份數據庫到 ${BACKUP_FILE}..."
            
            # 需要從環境變數獲取資料庫連接資訊
            if [ -f ".env" ]; then
                source .env
            fi
            
            # 嘗試從 MySQL 容器備份（如果有）
            if docker ps --format '{{.Names}}' | grep -q "mysql"; then
                MYSQL_CONTAINER=$(docker ps --format '{{.Names}}' | grep mysql | head -1)
                docker exec ${MYSQL_CONTAINER} mysqldump -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE} > ${BACKUP_FILE} 2>/dev/null || true
            else
                # 如果有外部資料庫，提示用戶手動備份
                print_warning "無法自動備份外部資料庫"
                print_info "請手動備份資料庫："
                echo "mysqldump -u ${MYSQL_USER:-username} -p ${MYSQL_DATABASE:-stock_note_project} > ${BACKUP_FILE}"
            fi
        fi
    else
        # 本地環境 - 假設可以直接連接 MySQL
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        print_info "備份本地數據庫到 ${BACKUP_FILE}..."
        
        # 嘗試備份（可能失敗，但不要中斷）
        if command -v mysqldump &> /dev/null; then
            if [ -f ".env" ]; then
                source .env
                mysqldump -u ${MYSQL_USER:-snote} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE:-stock_note_project} > ${BACKUP_FILE} 2>/dev/null || true
            fi
        fi
    fi
    
    if [ -f "${BACKUP_FILE}" ] && [ -s "${BACKUP_FILE}" ]; then
        print_success "資料庫已備份到: ${BACKUP_FILE}"
    else
        print_warning "自動備份失敗，請手動備份資料庫"
    fi
}

# 函數：更新代碼
update_code() {
    print_step "步驟 2: 更新代碼"
    
    if [ -d ".git" ]; then
        print_info "檢測到 Git 版本控制，更新代碼..."
        
        # 檢查是否有未提交的變更
        if [ -n "$(git status -s)" ]; then
            print_warning "發現未提交的變更"
            read -p "是否先提交變更？(y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_info "請手動提交變更後再執行升級"
                exit 1
            fi
        fi
        
        # 拉取最新代碼
        print_info "拉取最新代碼..."
        git pull
        
        print_success "代碼更新完成"
    else
        print_warning "未檢測到 Git，請手動更新代碼"
    fi
}

# 函數：更新依賴
update_dependencies() {
    print_step "步驟 3: 更新依賴"
    
    if check_docker; then
        print_info "使用 Docker，依賴會在重新建構時更新"
    else
        if [ -f "requirements.txt" ]; then
            print_info "更新 Python 依賴..."
            pip install -r requirements.txt --upgrade
            print_success "依賴更新完成"
        fi
    fi
}

# 函數：執行數據庫遷移
run_migration() {
    print_step "步驟 4: 執行數據庫遷移"
    
    if check_docker; then
        print_info "在 Docker 環境中執行遷移..."
        
        CONTAINER_NAME="stock-note-app"
        
        # 確保容器運行
        if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            print_info "啟動容器..."
            docker start ${CONTAINER_NAME} || docker-compose up -d
            sleep 3
        fi
        
        # 執行遷移
        if docker exec ${CONTAINER_NAME} python migrate.py status > /dev/null 2>&1; then
            docker exec ${CONTAINER_NAME} python migrate.py migrate
            print_success "數據庫遷移完成"
            docker exec ${CONTAINER_NAME} python migrate.py status
        else
            print_error "無法在容器中執行遷移"
            exit 1
        fi
    else
        print_info "在本地環境執行遷移..."
        
        if [ -f "migrate.py" ]; then
            python3 migrate.py status
            python3 migrate.py migrate
            print_success "數據庫遷移完成"
            python3 migrate.py status
        else
            print_error "找不到 migrate.py"
            exit 1
        fi
    fi
}

# 函數：重啟服務
restart_service() {
    print_step "步驟 5: 重啟服務"
    
    if check_docker; then
        print_info "重啟 Docker 容器..."
        
        if [ -f "docker-compose.yml" ] && docker-compose ps | grep -q "Up"; then
            docker-compose restart
            print_success "容器已重啟"
        elif [ -f "docker-compose.yml" ]; then
            docker-compose up -d --build
            print_success "容器已重新建構並啟動"
        else
            print_info "未使用 docker-compose，跳過重啟"
        fi
    else
        print_info "本地環境，請手動重啟應用"
        print_info "使用 gunicorn 或 supervisor 等工具重啟服務"
    fi
}

# 函數：驗證升級
verify_upgrade() {
    print_step "步驟 6: 驗證升級"
    
    if check_docker; then
        CONTAINER_NAME="stock-note-app"
        
        print_info "檢查容器狀態..."
        docker ps | grep ${CONTAINER_NAME} || print_error "容器未運行"
        
        print_info "檢查應用日誌..."
        docker-compose logs --tail=20 python-app
        
        print_info "檢查數據庫連接..."
        docker exec ${CONTAINER_NAME} python check_database.py || print_error "數據庫連接失敗"
    else
        print_info "檢查數據庫連接..."
        python3 check_database.py || print_error "數據庫連接失敗"
    fi
    
    print_success "升級驗證完成"
}

# 主流程
main() {
    echo ""
    print_info "開始版本升級流程..."
    echo ""
    
    # 確認是否繼續
    read -p "確定要執行版本升級嗎？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "升級已取消"
        exit 0
    fi
    
    echo ""
    
    # 執行升級步驟
    backup_database
    echo ""
    
    update_code
    echo ""
    
    update_dependencies
    echo ""
    
    run_migration
    echo ""
    
    restart_service
    echo ""
    
    verify_upgrade
    echo ""
    
    print_success "╔════════════════════════════════════════════╗"
    print_success "║    版本升級完成！                         ║"
    print_success "╚════════════════════════════════════════════╝"
    echo ""
    print_info "請訪問 http://localhost:5001 驗證應用是否正常運行"
}

# 執行主流程
main

