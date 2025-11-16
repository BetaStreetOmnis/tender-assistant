#!/bin/bash

echo "🚀 启动AI标书助理系统"
echo "========================="

# 检查是否在项目根目录
if [ ! -f "README.md" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo "📦 检查依赖..."

# 检查Python依赖
if [ ! -d "backend/venv" ] && [ ! -d ".venv" ]; then
    echo "🔧 创建Python虚拟环境..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 检查Node.js依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "🔧 安装前端依赖..."
    cd frontend
    npm install || yarn install
    cd ..
fi

echo "🔧 初始化数据库..."
cd backend
source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null
python scripts/init_database.py
cd ..

echo ""
echo "🎯 启动服务..."
echo "后端服务: http://localhost:8000"
echo "前端服务: http://localhost:3000"
echo "API文档: http://localhost:8000/docs"
echo ""

# 启动后端服务
echo "🔧 启动后端服务..."
cd backend
source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端服务
echo "🔧 启动前端服务..."
cd frontend
yarn dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 系统启动成功！"
echo "========================="
echo "前端: http://localhost:3000"
echo "后端: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 等待用户中断
trap 'echo ""; echo "🛑 正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo "✅ 服务已停止"; exit 0' INT

wait