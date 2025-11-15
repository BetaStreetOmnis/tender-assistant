# AI标书助理系统

**Tender Assistant** - 基于AI的智能招投标文档管理系统

## 项目概述

AI标书助理系统是一个基于人工智能技术的招投标文档管理平台，集成了知识库管理、文档智能生成、投标检查等核心功能。

### 核心功能

- 📄 **招标文件智能解析**：自动提取招标文件关键信息
- 🔍 **智能检索与问答**：基于RAG的智能问答系统
- 📝 **投标文档自动生成**：AI辅助生成投标响应文档
- ✅ **智能检查引擎**：废标项检查、一致性检查、完整性检查
- 📚 **模板管理系统**：投标模板库管理与复用
- 🎯 **知识图谱查询**：实体关系查询与分析

### 技术架构

- **后端**：FastAPI + SQLAlchemy + Celery
- **前端**：Vue 3 + TypeScript + Ant Design Vue
- **数据库**：PostgreSQL + Redis + Milvus + Neo4j（可选）
- **AI能力**：LLM集成（支持通义千问、Deepseek等）

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- （可选）Milvus 2.0+
- （可选）Neo4j 4.0+

### 后端安装

```bash
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 初始化数据库
python scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端安装

```bash
cd frontend
npm install

# 启动开发服务器
npm run dev
```

## 项目结构

```
tender-assistant/
├── backend/                # 后端服务
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── knowledge/     # 知识库模块（JetLinks复用85%）
│   │   ├── docgen/        # 文档生成模块（DocuGen复用70%）
│   │   ├── business/      # 业务逻辑模块（新开发）
│   │   ├── models/        # 数据模型
│   │   └── services/      # 业务服务
│   └── storage/           # 文件存储
├── frontend/              # 前端应用
│   └── src/
│       ├── views/         # 页面组件
│       └── components/    # 通用组件
├── docs/                  # 文档
└── scripts/               # 脚本
```

## 核心模块

### 知识库模块（Knowledge）
基于JetLinks-Knowledge，提供：
- 多模态文档解析（PDF/Word/图片）
- 9种智能搜索模式
- 向量检索与知识图谱
- RAG检索增强生成

### 文档生成模块（DocGen）
基于DocuGen改进，提供：
- 模板管理与变量替换
- AI大纲与内容生成
- Word文档格式化输出
- 流式内容生成

### 业务逻辑模块（Business）
新开发，提供：
- 招标项目管理
- 投标响应管理
- 智能检查引擎
- 工作流管理

## 开发计划

- ✅ Phase 1: 基础架构搭建（2周）
- ⏳ Phase 2: 核心功能开发（6周）
- ⏳ Phase 3: 智能功能开发（4周）
- ⏳ Phase 4: 完善优化部署（2周）

## 文档

- [完整实施方案](../AI标书助理系统-完整实施方案.md)
- [代码库分析报告](../标书助理系统-代码库分析报告.md)
- [API文档](docs/api.md)
- [架构文档](docs/architecture.md)

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系开发团队。

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**# tender-assistant
