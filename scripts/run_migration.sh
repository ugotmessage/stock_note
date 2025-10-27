#!/bin/bash

# 數據庫遷移執行腳本
# 用於快速執行數據庫遷移

set -e  # 遇到錯誤立即退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函數：打印彩色消息
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

# 檢查是否在正確的目錄
if [ ! -f "migrate.py" ]; then
    print_error "請在專案根目錄執行此腳本"
    exit 1
fi

# 檢查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    print_error "找不到 Python 3"
    exit 1
fi

# 檢查配置文件
if [ ! -f "config.py" ]; then
    print_error "找不到 config.py"
    exit 1
fi

print_info "開始檢查數據庫連接..."

# 檢查數據庫連接
if python3 check_database.py; then
    print_success "數據庫連接正常"
else
    print_error "數據庫連接失敗，請檢查配置"
    exit 1
fi

echo ""
print_info "執行遷移前，顯示當前狀態："
python3 migrate.py status

echo ""
read -p "是否繼續執行遷移？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "遷移已取消"
    exit 0
fi

echo ""
print_info "開始執行數據庫遷移..."

# 執行遷移
if python3 migrate.py migrate; then
    print_success "遷移執行完成"
    echo ""
    print_info "當前遷移狀態："
    python3 migrate.py status
else
    print_error "遷移執行失敗"
    exit 1
fi

print_success "完成！"

