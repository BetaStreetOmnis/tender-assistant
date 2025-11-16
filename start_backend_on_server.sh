#!/bin/bash
# 在服务器上手动执行此脚本来启动修复后的后端服务

echo "🔄 启动tender-assistant后端服务"
echo "================================"

# 1. 停止旧服务
echo "🛑 停止旧服务..."
pkill -f 'complete_fixed_backend.py' 2>/dev/null || true
pkill -f 'python.*8000' 2>/dev/null || true
sleep 2

# 2. 检查文件
echo "📁 检查文件..."
ls -lh /opt/tender-assistant/complete_fixed_backend.py

# 3. 测试Python能否导入依赖
echo "🧪 测试Python依赖..."
cd /opt/tender-assistant
python3 -c "import fastapi; import uvicorn; import pydantic; print('✅ 依赖正常')" || echo "❌ 缺少依赖"

# 4. 尝试直接启动（前台模式，查看错误）
echo "🚀 启动服务（前台模式，查看错误）..."
echo "按 Ctrl+C 停止前台模式，然后重新运行后台模式"
python3 complete_fixed_backend.py

# 如果上面的前台启动成功，按Ctrl+C后，执行后台启动：
# nohup python3 complete_fixed_backend.py > backend.log 2>&1 &

# 验证服务
# curl -s http://127.0.0.1:8000/api/v1/health
