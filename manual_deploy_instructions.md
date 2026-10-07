# 手动部署修复后的tender-assistant后端

> 历史部署记录：本文中的 `43.160.192.153` 和 `3010` 属于旧部署，该机器列入退订计划。这些命令不代表当前可用入口；部署时请填写实际服务器和端口，并验证 API 路由。

由于SSH权限问题，需要手动执行以下命令来部署修复后的后端服务：

## 1. 连接到服务器
```bash
ssh root@43.160.192.153
# 使用本机 SSH 认证配置；公开文档不记录登录密码。
```

## 2. 停止现有服务
```bash
cd /opt/tender-assistant
pkill -f "complete_fixed_backend.py" || true
pkill -f "uvicorn.*8000" || true
```

## 3. 备份现有文件
```bash
cp complete_fixed_backend.py complete_fixed_backend.py.backup.$(date +%Y%m%d_%H%M%S)
```

## 4. 从本地上传修复后的代码
在本地执行：
```bash
scp /Users/chenhao/Desktop/code/tender-assistant/complete_fixed_backend.py root@43.160.192.153:/opt/tender-assistant/
```

## 5. 在服务器上启动新服务
```bash
cd /opt/tender-assistant
python3 complete_fixed_backend.py > backend.log 2>&1 &
```

## 6. 验证服务
```bash
# 检查进程
ps aux | grep "complete_fixed_backend.py" | grep -v grep

# 测试API
curl -s http://127.0.0.1:8000/api/v1/health | python3 -m json.tool

# 查看日志
tail -f backend.log
```

## 7. 测试代理访问
```bash
# 在本地测试3010端口代理
curl -s http://43.160.192.153:3010/api/v1/health
```

## 修复内容
修复后的后端包含以下功能：
- ✅ 健康检查端点 (/api/v1/health)
- ✅ 分析功能 (/api/v1/bidding/analyze)
- ✅ 模板列表 (/api/v1/template/list)
- ✅ **新增**: 生成大纲功能 (/api/v1/bidding/generate-outline)
- ✅ 支持JSON和表单请求格式
- ✅ 完整的错误处理机制
- ✅ 运行在8000端口（与Nginx代理配置一致）