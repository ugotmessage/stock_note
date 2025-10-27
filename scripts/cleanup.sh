#!/bin/bash

# 專案清理腳本
# 用於移除過時和重複的文件

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo -e "${BLUE}►${NC} $1"
}

# 顯示清理提示
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    專案結構清理腳本                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
print_info "此腳本將移除過時和重複的文件"
echo ""

# 要移除的文件清單
FILES_TO_REMOVE=(
    "init_database.sql"           # 舊的初始化腳本
    "update_database.sql"         # 舊的更新腳本
    "test_ajax.html"              # 測試 HTML
    "test_header_sort.html"       # 測試 HTML
    "test_styles.html"            # 測試 HTML
)

# 可選移除的文件
OPTIONAL_FILES=(
    "test_notes_functionality.py" # 測試腳本
    "db_test.py"                  # 數據庫測試
)

# 顯示要移除的文件
print_step "將移除以下文件："
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        print_warning "  - $file"
    fi
done
echo ""

# 顯示可選移除的文件
print_step "可選移除的文件（請手動選擇）："
for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_info "  - $file"
    fi
done
echo ""

# 確認
read -p "確定要執行清理嗎？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "清理已取消"
    exit 0
fi

echo ""

# 創建備份目錄
BACKUP_DIR="_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
print_info "備份目錄: $BACKUP_DIR"

# 移除文件
REMOVED_COUNT=0
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        # 備份
        cp "$file" "$BACKUP_DIR/"
        # 移除
        rm -f "$file"
        print_success "已移除: $file"
        REMOVED_COUNT=$((REMOVED_COUNT + 1))
    else
        print_info "文件不存在: $file"
    fi
done

echo ""

# 處理可選文件
print_step "處理可選文件..."
for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        read -p "是否移除 $file? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp "$file" "$BACKUP_DIR/"
            rm -f "$file"
            print_success "已移除: $file"
            REMOVED_COUNT=$((REMOVED_COUNT + 1))
        fi
    fi
done

echo ""

# 總結
if [ $REMOVED_COUNT -gt 0 ]; then
    print_success "清理完成！共移除 $REMOVED_COUNT 個文件"
    print_info "備份位置: $BACKUP_DIR"
    echo ""
    print_info "清理後建議執行："
    echo "  1. python migrate.py status  # 檢查遷移狀態"
    echo "  2. git add -A                 # 提交更改"
    echo "  3. git commit -m '清理過時文件'"
else
    print_info "沒有文件需要移除"
fi

echo ""

