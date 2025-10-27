#!/bin/bash

# 在 Docker 容器中執行數據庫遷移

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

# 檢查 Docker 是否運行
if ! docker info &> /dev/null; then
    print_error "Docker 未運行，請先啟動 Docker"
    exit 1
fi

# 檢查容器是否存在
CONTAINER_NAME="stock-note-app"

if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_error "找不到容器 ${CONTAINER_NAME}"
    print_info "請先啟動容器: docker-compose up -d"
    exit 1
fi

# 檢查容器是否運行
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_warning "容器未運行，正在啟動..."
    docker start ${CONTAINER_NAME}
    sleep 2
fi

print_info "在 Docker 容器中執行遷移..."

# 執行遷移
if docker exec ${CONTAINER_NAME} python migrate.py status; then
    print_success "連接容器成功"
    
    if docker exec ${CONTAINER_NAME} python migrate.py migrate; then
        print_success "遷移執行完成"
        docker exec ${CONTAINER_NAME} python migrate.py status
    else
        print_error "遷移執行失敗"
        exit 1
    fi
else
    print_error "無法連接到容器"
    exit 1
fi

print_success "完成！"

