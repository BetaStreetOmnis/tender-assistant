# AI标书助理系统 - 开发指南

## 开发环境搭建

### 1. 克隆项目
```bash
git clone <repository-url>
cd tender-assistant
```

### 2. 后端环境
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件配置环境变量
```

### 3. 前端环境
```bash
cd frontend
npm install
```

### 4. 使用Docker（推荐）
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 开发流程

### 后端开发
1. 启动服务：`uvicorn app.main:app --reload`
2. 访问API文档：http://localhost:8000/docs
3. 数据库迁移：`alembic upgrade head`

### 前端开发
1. 启动服务：`npm run dev`
2. 访问应用：http://localhost:3000
3. 类型检查：`npm run type-check`

## 项目结构说明

### 后端模块
- `knowledge/`: 知识库模块（复用JetLinks-Knowledge 85%）
- `docgen/`: 文档生成模块（复用DocuGen 70%）
- `business/`: 业务逻辑模块（新开发）

### 前端页面
- `dashboard/`: 工作台
- `tender/`: 招标管理
- `bidding/`: 投标管理
- `template/`: 模板管理

## API接口

### 招标管理
- `POST /api/v1/tender/upload` - 上传招标文件
- `GET /api/v1/tender/projects` - 获取项目列表
- `POST /api/v1/tender/projects/{id}/analyze` - 分析需求

### 投标管理
- `POST /api/v1/bidding/responses` - 创建投标响应
- `POST /api/v1/bidding/responses/{id}/generate` - 生成文档
- `POST /api/v1/bidding/responses/{id}/check` - 智能检查

## 下一步开发

### Phase 1: 基础功能（2周）
- [ ] 完善数据库模型
- [ ] 实现文件上传功能
- [ ] 集成JetLinks知识库
- [ ] 集成DocuGen文档生成

### Phase 2: 核心功能（6周）
- [ ] 招标文件解析
- [ ] 模板管理系统
- [ ] AI内容生成
- [ ] 智能检查引擎

### Phase 3: 前端界面（4周）
- [ ] 工作台界面
- [ ] 招标管理页面
- [ ] 投标编辑器
- [ ] 检查报告页面

## 代码规范

### Python
- 使用Black格式化
- 遵循PEP 8标准
- 类型注解必需

### TypeScript/Vue
- 使用Prettier格式化
- 遵循ESLint规则
- Composition API优先

## 部署说明

### 开发环境
```bash
docker-compose up -d
```

### 生产环境
1. 配置环境变量
2. 构建镜像
3. 使用Kubernetes部署