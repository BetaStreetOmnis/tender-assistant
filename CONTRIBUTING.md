# 贡献指南

感谢你对 AI 标书助理感兴趣！🎉

## 🐛 提交 Bug

1. 先搜索 [Issues](https://github.com/BetaStreetOmnis/tender-assistant/issues) 确认没有重复
2. 点击 "New Issue"
3. 使用 Bug 模板填写

## 💡 功能建议

1. 在 Issues 中提交 Feature Request
2. 描述清楚需求和使用场景

## 🔧 提交代码

### 开发环境

```bash
# Fork 并克隆
git clone https://github.com/YOUR_USERNAME/tender-assistant.git
cd tender-assistant

# 安装依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 创建分支
git checkout -b feature/your-feature
```

### 代码规范

- **Python**: 遵循 PEP 8，使用 `black` 格式化
- **Vue/TypeScript**: 遵循 ESLint 配置
- 提交信息: 使用约定式提交

```
feat: 添加用户登录功能
fix: 修复文档上传错误
docs: 更新安装文档
refactor: 重构服务层
test: 添加单元测试
```

### 提交 PR

1. Push 到你的 fork
2. 在 GitHub 创建 Pull Request
3. 等待 review

## 📋 行为准则

- 尊重所有贡献者
- 建设性讨论
- 关注问题本身，不是人

## 📄 许可证

提交代码即表示同意以 MIT 许可证授权。
