#!/bin/bash

echo "🔄 重启AI标书助理系统后端服务"

# 1. 停止旧的服务
echo "⏹️ 停止旧的Python服务..."
pkill -f "python.*complete_fixed_backend.py" || echo "没有运行中的服务"
pkill -f "uvicorn.*8000" || echo "没有运行中的uvicorn服务"
sleep 2

# 2. 检查端口占用
echo "🔍 检查8000端口..."
PORT_CHECK=$(lsof -i:8000 | grep LISTEN || echo "端口空闲")
echo "$PORT_CHECK"

# 3. 备份旧文件
if [ -f "/opt/tender-assistant/complete_fixed_backend.py" ]; then
    echo "💾 备份旧文件..."
    cp /opt/tender-assistant/complete_fixed_backend.py /opt/tender-assistant/complete_fixed_backend.py.backup.$(date +%Y%m%d_%H%M%S)
fi

# 4. 复制新文件
echo "📋 复制修复后的代码..."
cp /Users/chenhao/Desktop/code/tender-assistant/complete_fixed_backend.py /opt/tender-assistant/

# 5. 切换到目录
cd /opt/tender-assistant

# 6. 启动新服务
echo "🚀 启动新服务..."
nohup python3 complete_fixed_backend.py > /opt/tender-assistant/backend.log 2>&1 &

# 等待服务启动
sleep 3

# 7. 检查服务状态
echo "✅ 检查服务状态..."
ps aux | grep "complete_fixed_backend.py" | grep -v grep

# 8. 测试API
echo "🧪 测试API端点..."
curl -s http://127.0.0.1:8000/api/v1/health | python3 -m json.tool || echo "API测试失败"

echo ""
echo "📋 查看日志: tail -f /opt/tender-assistant/backend.log"
echo "📋 检查进程: ps aux | grep complete_fixed_backend"
echo "📋 测试服务: curl http://127.0.0.1:8000/api/v1/health"
