<div align="center">

# 🏢 AI 标书助理

**智能招投标文档管理平台** — 让 AI 帮你搞定标书

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Vue](https://img.shields.io/badge/Vue-3.4+-green.svg)](https://vuejs.org)

</div>

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 📄 **招标文件解析** | 自动提取招标文件关键信息（截止时间、资质要求、评分标准） |
| 🤖 **AI 智能问答** | 基于招标文档，回答任何问题（RAG） |
| 📝 **投标文档生成** | AI 辅助生成投标响应文档 |
| ✅ **智能检查** | 废标项检查、一致性检查、完整性检查 |
| 📚 **模板管理** | 投标模板库管理与复用 |
| 🔍 **知识图谱** | 招标实体关系查询（可选） |

---

## 🚀 快速开始

### 环境要求

| 组件 | 版本 | 必需 |
|------|------|------|
| Python | 3.8+ | ✅ |
| Node.js | 16+ | ✅ |
| PostgreSQL | 12+ | ✅ |
| Redis | 6+ | ✅ |
| Milvus | 2.0+ | 可选 |
| Neo4j | 4.0+ | 可选 |

### 一键启动（开发模式）

```bash
# 克隆项目
git clone https://github.com/BetaStreetOmnis/tender-assistant.git
cd tender-assistant

# 后端
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置数据库和 AI API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端（另一个终端）
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

---

## 🏗 项目结构

```
tender-assistant/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/         # API 路由
│   │   ├── knowledge/      # 知识库（JetLinks 复用 85%）
│   │   ├── docgen/         # 文档生成（DocuGen 复用 70%）
│   │   ├── business/       # 标书业务逻辑
│   │   ├── models/         # 数据模型
│   │   └── services/       # 业务服务
│   └── storage/            # 文件存储
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── views/          # 页面
│       └── components/     # 组件
├── docs/                   # 文档
└── scripts/               # 脚本
```

---

## 🔧 配置

### 环境变量（`.env`）

```bash
# 数据库
DATABASE_URL=postgresql://user:pass@localhost:5432/tender_assistant
REDIS_URL=redis://localhost:6379/0

# AI 模型（选择一个）
OPENAI_API_KEY=sk-xxx
DASHSCOPE_API_KEY=xxx  # 通义千问
DEEPSEEK_API_KEY=xxx    # DeepSeek

# 向量数据库（可选）
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

---

## 📖 API 文档

启动后访问：http://localhost:8000/docs

### 主要端点

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/tender/upload` | 上传招标文件 |
| GET | `/api/v1/tender/{id}` | 获取招标详情 |
| POST | `/api/v1/bidding/generate` | 生成投标文档 |
| POST | `/api/v1/check` | 智能检查 |
| POST | `/api/v1/chat` | AI 问答 |

---

## 🗺️ 开发路线图

- [x] Phase 1: 基础架构
- [x] Phase 2: 文档解析 + 知识库
- [ ] Phase 3: 投标文档生成
- [ ] Phase 4: 智能检查引擎
- [ ] Phase 5: 前端界面优化
- [ ] Phase 6: 部署 & Docker

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

[MIT License](LICENSE)

---

## 📞 联系

- 提交 [Issue](https://github.com/BetaStreetOmnis/tender-assistant/issues)
- Pull Request 欢迎！

---

<div align="center">

**⭐ 如果觉得有用，给个 Star！⭐**

Made with ❤️ by BetaStreetOmnis

</div>
