#!/bin/bash

# 红薯医生 Docker 部署脚本
# 使用方法: ./deploy.sh [http|https]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置
DOMAIN="redbook.fffup.asia"
PROJECT_DIR="/opt/red-book-agent"

echo -e "${GREEN}=== 红薯医生 Docker 部署脚本 ===${NC}"
echo ""

# 检查是否在项目目录
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env.prod" ]; then
    echo -e "${YELLOW}警告: 未找到 .env.prod 文件${NC}"
    echo "正在创建 .env.prod 文件..."
    cp .env.example .env.prod
    echo -e "${YELLOW}请编辑 .env.prod 文件，填入你的 API Key${NC}"
    echo "nano .env.prod"
    exit 1
fi

# 检查 API Key 是否配置
if ! grep -q "OPENAI_API_KEY=" .env.prod || grep -q "OPENAI_API_KEY=$" .env.prod; then
    echo -e "${RED}错误: 请在 .env.prod 中配置 OPENAI_API_KEY${NC}"
    echo "nano .env.prod"
    exit 1
fi

# 选择部署模式
DEPLOY_MODE=${1:-http}

if [ "$DEPLOY_MODE" = "https" ]; then
    echo -e "${GREEN}部署模式: HTTPS (需要 SSL 证书)${NC}"
    
    # 检查 SSL 证书
    if [ ! -f "nginx/ssl/fullchain.pem" ] || [ ! -f "nginx/ssl/privkey.pem" ]; then
        echo -e "${RED}错误: 未找到 SSL 证书文件${NC}"
        echo "请将证书文件放置在 nginx/ssl/ 目录下:"
        echo "  - nginx/ssl/fullchain.pem"
        echo "  - nginx/ssl/privkey.pem"
        echo ""
        echo "或者使用 HTTP 模式部署: ./deploy.sh http"
        exit 1
    fi
    
    # 使用 HTTPS 配置
    rm -f nginx/conf.d/redbook-http.conf
    echo -e "${GREEN}✓ SSL 证书检查通过${NC}"
else
    echo -e "${GREEN}部署模式: HTTP${NC}"
    # 使用 HTTP 配置
    rm -f nginx/conf.d/redbook.conf
    echo -e "${GREEN}✓ 使用 HTTP 模式${NC}"
fi

# 停止旧容器
echo ""
echo -e "${YELLOW}停止旧容器...${NC}"
docker-compose --env-file .env.prod down 2>/dev/null || true

# 构建并启动容器
echo ""
echo -e "${YELLOW}构建并启动容器...${NC}"
docker-compose --env-file .env.prod up -d --build

# 等待服务启动
echo ""
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查容器状态
echo ""
echo -e "${GREEN}=== 容器状态 ===${NC}"
docker-compose ps

# 检查服务健康状态
echo ""
echo -e "${GREEN}=== 服务健康检查 ===${NC}"
sleep 5

# 检查后端服务
if curl -s http://localhost:8002/api/health > /dev/null; then
    echo -e "${GREEN}✓ 后端服务正常${NC}"
else
    echo -e "${RED}✗ 后端服务异常${NC}"
fi

# 检查前端服务
if curl -s http://localhost:8100 > /dev/null; then
    echo -e "${GREEN}✓ 前端服务正常${NC}"
else
    echo -e "${RED}✗ 前端服务异常${NC}"
fi

# 显示访问信息
echo ""
echo -e "${GREEN}=== 部署完成 ===${NC}"
echo ""
echo "访问地址:"
if [ "$DEPLOY_MODE" = "https" ]; then
    echo "  - 前端: https://$DOMAIN"
    echo "  - 后端API: https://$DOMAIN/api"
else
    echo "  - 前端: http://$DOMAIN"
    echo "  - 后端API: http://$DOMAIN/api"
fi
echo ""
echo "常用命令:"
echo "  - 查看日志: docker-compose logs -f"
echo "  - 停止服务: docker-compose down"
echo "  - 重启服务: docker-compose restart"
echo "  - 重新构建: docker-compose --env-file .env.prod up -d --build"
echo ""
echo -e "${GREEN}✓ 部署成功！${NC}"
