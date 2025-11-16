# AI标书助理系统 - 项目配置与启动指南

## 📋 项目概述

AI标书助理系统是一个基于FastAPI + Vue3的智能投标文档生成平台，集成DocuGen功能，提供招标文档分析、投标大纲生成、完整文档AI生成等功能。

## 🏗️ 系统架构

### 后端技术栈
- **框架**: FastAPI (Python 3.13)
- **数据库**: MySQL 8.0 (腾讯云)
- **缓存**: Redis (外部服务器)
- **向量数据库**: Milvus (外部服务器)
- **AI模型**: 智谱GLM-4.6
- **文档处理**: DocuGen

### 前端技术栈
- **框架**: Vue 3.4 + TypeScript
- **构建工具**: Vite 5.0
- **UI组件**: Element Plus
- **状态管理**: Pinia
- **图表库**: ECharts

## 🔧 环境配置

### 数据库配置
```env
# MySQL配置
DB_HOST=cd-cynosdbmysql-grp-ajwkswr8.sql.tencentcdb.com
DB_PORT=24254
DB_USER=root
DB_PASSWORD=c3676860!
DB_NAME=tender_assistant
```

### Redis配置
```env
# Redis配置
REDIS_HOST=1.14.62.40
REDIS_PORT=26739
REDIS_PASSWORD=3676860
REDIS_DB=0
```

### AI模型配置
```env
# 智谱GLM配置
LLM_API_KEY=ba4c4317831947cbb697e7ad68393308.qdUFMMBgGg8wtqHc
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
LLM_MODEL=glm-4.6

# OpenAI兼容API
OPENAI_API_KEY=ba4c4317831947cbb697e7ad68393308.qdUFMMBgGg8wtqHc
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
```

## 🚀 快速启动

### 方法1: 使用启动脚本
```bash
# 在项目根目录运行
./start.sh
```

### 方法2: 手动启动

#### 1. 启动后端
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. 启动前端
```bash
cd frontend
yarn install
yarn dev
```

## 📱 访问地址

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 🗄️ 数据库初始化

首次运行需要初始化数据库：

```bash
cd backend
python scripts/init_database.py
```

## 📊 功能模块

### 1. 投标管理
- 投标项目创建和编辑
- 项目状态跟踪
- 响应文档管理

### 2. 模板管理
- 模板上传和管理
- 变量配置
- 模板预览

### 3. 智能生成
- 招标文档分析
- 投标大纲生成
- 完整文档生成

### 4. 数据统计
- 项目统计图表
- 趋势分析
- 活动记录

## 🔗 API接口

### 投标管理API
```
GET    /api/v1/bidding/demo                    # 演示接口
GET    /api/v1/bidding/responses              # 获取投标列表
POST   /api/v1/bidding/responses              # 创建投标
GET    /api/v1/bidding/responses/{id}         # 获取投标详情
POST   /api/v1/bidding/analyze-tender         # 分析招标文档
POST   /api/v1/bidding/generate-outline       # 生成大纲
POST   /api/v1/bidding/generate-document      # 生成文档
```

### 模板管理API
```
GET    /api/v1/template/list                   # 获取模板列表
POST   /api/v1/template/upload                 # 上传模板
GET    /api/v1/template/variables              # 获取模板变量
POST   /api/v1/template/generate-from-template # 基于模板生成
```

### 系统API
```
GET    /                                     # 系统信息
GET    /health                               # 健康检查
```

## 🎯 开发指南

### 添加新功能
1. 在 `backend/app/api/v1/` 添加新的路由文件
2. 在 `backend/app/models/` 添加数据模型
3. 在 `backend/app/schemas/` 添加请求/响应模式
4. 在 `frontend/src/views/` 添加前端页面
5. 在 `frontend/src/api/` 添加API调用
6. 在 `frontend/src/stores/` 添加状态管理

### 代码规范
- 后端遵循Python PEP8规范
- 前端使用TypeScript严格模式
- 提交前运行linting检查

## 🔧 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 检查数据库配置
cat backend/.env | grep DB_

# 测试连接
python -c "import pymysql; pymysql.connect(host='your-host', user='your-user', password='your-password')"
```

#### 2. Redis连接失败
```bash
# 检查Redis配置
cat backend/.env | grep REDIS

# 测试连接
redis-cli -h your-redis-host -p your-redis-port -a your-password
```

#### 3. 前端API调用失败
- 确认后端服务正在运行
- 检查前端代理配置 `vite.config.ts`
- 查看浏览器网络面板的错误信息

#### 4. AI模型调用失败
- 检查API密钥配置
- 确认网络连接
- 查看后端日志

### 日志查看
```bash
# 后端日志
tail -f backend/logs/app.log

# 前端开发服务器日志
# 查看运行yarn dev的终端输出
```

## 📦 部署说明

### 生产环境部署
1. 配置生产环境变量
2. 构建前端: `yarn build`
3. 启动后端: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. 配置反向代理(Nginx)
5. 配置SSL证书

### Docker部署
```bash
# 构建镜像
docker build -t tender-assistant .

# 运行容器
docker run -p 8000:8000 tender-assistant
```

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📞 技术支持

- 项目文档: `README.md`
- API文档: http://localhost:8000/docs
- 问题反馈: 通过GitHub Issues

---

**注意**: 确保所有外部服务(MySQL、Redis、Milvus)正常运行，并正确配置环境变量。