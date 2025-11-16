# AI标书助理系统 - 前端

基于Vue3 + TypeScript + Element Plus构建的智能投标文档生成平台前端应用。

## 🚀 技术栈

- **框架**: Vue 3.4+
- **语言**: TypeScript 5.3+
- **构建工具**: Vite 5.0+
- **UI组件库**: Element Plus 2.4+
- **状态管理**: Pinia 2.1+
- **路由**: Vue Router 4.2+
- **HTTP客户端**: Axios 1.6+
- **图表库**: ECharts 5.4+
- **图标库**: Element Plus Icons Vue

## 📁 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口
│   │   ├── index.ts       # HTTP客户端配置
│   │   ├── bidding.ts     # ��标相关API
│   │   ├── template.ts    # 模板相关API
│   │   └── system.ts      # 系统相关API
│   ├── components/        # 公共组件 (待扩展)
│   ├── router/            # 路由配置
│   │   └── index.ts
│   ├── stores/            # Pinia状态管理
│   │   ├── bidding.ts     # 投标状态管理
│   │   └── template.ts    # 模板状态管理
│   ├── types/             # TypeScript类型定义
│   │   └── index.ts
│   ├── views/             # 页面组件
│   │   ├── Home.vue       # 首页
│   │   ├── Dashboard.vue  # 仪表板
│   │   ├── Bidding.vue    # 投标管理
│   │   ├── Templates.vue  # 模板管理
│   │   ├── Generate.vue   # 文档生成
│   │   ├── Analyze.vue    # 招标分析
│   │   ├── Settings.vue   # 系统设置
│   │   └── NotFound.vue   # 404页面
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口
├── index.html             # HTML模板
├── package.json           # 项目依赖
├── tsconfig.json          # TypeScript配置
├── vite.config.ts         # Vite配置
└── README.md              # 项目说明
```

## 🛠️ 安装和运行

### 环境要求

- Node.js 18.0+
- npm 9.0+ 或 yarn 1.22+

### 安装依赖

```bash
cd frontend
npm install
# 或
yarn install
```

### 启动开发服务器

```bash
npm run dev
# 或
yarn dev
```

应用将在 `http://localhost:3000` 启动

### 构建生产版本

```bash
npm run build
# 或
yarn build
```

### 预览生产构建

```bash
npm run preview
# 或
yarn preview
```

## 🎯 功能特性

### 核心功能

- **投标管理**: 创建、编辑、查看投标项目
- **模板管理**: 上传、管理、使用投标模板
- **智能生成**: 基于模板和AI生成投标文档
- **招标分析**: AI分析招标文档提取关键要点
- **数据统计**: 投标项目统计和趋势分析
- **系统设置**: 系统信息查看和配置管理

### 技术特性

- **类型安全**: 完整的TypeScript类型定义
- **响应式设计**: 适配不同屏幕尺寸
- **状态管理**: 使用Pinia进行集中状态管理
- **路由守卫**: 路由权限和导航控制
- **API封装**: 统一的HTTP请求处理
- **错误处理**: 全局错误捕获和用户提示
- **加载状态**: 优雅的加载和过渡动画

## 📱 页面说明

### 首页 (/)
- 系统概览和快速操作入口
- 最新投标项目展示
- 系统状态监控

### 仪表板 (/dashboard)
- 投标数据统计图表
- 项目状态��布
- 月度趋势分析
- 最新活动记录

### 投标管理 (/bidding)
- 投标项目列表管理
- 状态筛选和搜索
- 投标详情查看
- 项目操作（编辑、复制、删除等）

### 模板管理 (/templates)
- 模板列表展示
- 模板上传和管理
- 变量配置和预览
- 模板使用统计

### 文档生成 (/generate)
- 分步骤文档生成流程
- 模板选择和变量填写
- 实时预览和结果下载
- 生成进度监控

### 招标分析 (/analyze)
- 招标文档内容输入
- AI智能分析处理
- 关键要点提取
- 分析结果保存

### 系统设置 (/settings)
- 系统信息查看
- API端点管理
- 健康状态检查
- 缓存清理操作

## 🔧 配置说明

### API配置

API基础URL在 `vite.config.ts` 中配置：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000', // 后端服务地址
      changeOrigin: true,
      secure: false
    }
  }
}
```

### 环境变量

可以创建 `.env.local` 文件来配置环境变量：

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=AI标书助理系统
```

## 🤝 开发指南

### 添加新的API接口

1. 在 `src/types/index.ts` 中定义类型
2. 在 `src/api/` 中添加API函数
3. 在对应的store中添加状态管理逻辑

### 添加新页面

1. 在 `src/views/` 中创建页面组件
2. 在 `src/router/index.ts` 中添加路由
3. 在侧边栏菜单中添加导航项

### 状态管理

使用Pinia进行状态管理，每个主要功能模块都有对应的store文件：

- `bidding.ts`: 投标相关状态
- `template.ts`: 模板相关状态

## 🐛 常见问题

### 1. API请求失败
- 检查后端服务是否启动
- 确认API代理配置是否正确
- 查看浏览器开发者工具的网络面板

### 2. 类型错误
- 确保TypeScript版本兼容
- 检查类型定义是否完整
- 运行 `npm run lint` 检查代码规范

### 3. 构建失败
- 清除node_modules重新安装依赖
- 检查Node.js版本是否符合要求
- 查看构建日志中的错误信息

## 📝 待优化功能

- [ ] 添加用户认证和权限管理
- [ ] 实现文件拖拽上传
- [ ] 添加更多图表类型
- [ ] 优化移动端适配
- [ ] 添加国际化支持
- [ ] 实现主题切换功能
- [ ] 添加操作日志记录
- [ ] 优化性能和加载速度

## 📞 技术支持

如有技术问题，请查看：
1. 浏览器开发者工具的控制台
2. 网络请求面板
3. 构建日志信息

---

**注意**: 本项目为前端应用，需要配合后端服务一起使用。请确保后端服务正常运行后再启动前端应用。