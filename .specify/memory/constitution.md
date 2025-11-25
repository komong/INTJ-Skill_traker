# Skill Tracker Project Constitution

## Core Principles

### I. Documentation-First Development
每个功能开发前必须先编写规格文档（Spec）；
规格文档包含：目标、技术方案、验收标准；
文档驱动开发，确保需求清晰、方向明确。

### II. Incremental Implementation
大功能拆分为小阶段（Phase），逐步实现；
每个 Phase 完成后进行测试验证；
避免一次性实现过多功能，降低调试复杂度。

### III. Security-First
用户认证：JWT Token（24小时有效期）；
密码加密：bcrypt（salt rounds = 12）；
输入验证：XSS 过滤、SQL 注入防护；
所有 API 必须经过安全审查。

### IV. Data Integrity
双重存储：MySQL（云端）+ localStorage（离线）；
版本控制：数据变更使用版本号追踪；
冲突处理：基于版本号检测和解决；
自动同步：修改后 2 秒防抖自动同步到云端。

### V. Error Handling & Debugging
**防御性编程**：使用可选链 `?.` 和默认值 `||`；
**完整错误处理**：所有异步操作必须 try-catch；
**友好提示**：空数据状态需要明确的 UI 反馈；
**调试记录**：每次遇到问题必须记录到 TROUBLESHOOTING.md。

### VI. Code Quality
ESLint + Prettier 代码规范；
组件化开发：功能模块独立封装；
命名规范：语义化、见名知意；
注释完整：关键逻辑必须添加注释。

## Development Workflow

### 1. 功能开发流程
```
需求分析 → 编写 Spec → 拆分 Phase → 逐个实现 → 测试验证 → 文档更新
```

### 2. Git 工作流
- 功能分支命名：`feature/功能名称` 或 `00X-功能代号`
- 提交信息规范：
  - `feat:` 新功能
  - `fix:` Bug 修复
  - `docs:` 文档更新
  - `refactor:` 重构
  - `chore:` 工具配置
- 提交前检查：`.gitignore` 正确，无敏感信息

### 3. 调试流程
1. 查看浏览器控制台（Console + Network）
2. 检查后端日志（API 请求 + 数据库连接）
3. 分层排查（前端 → 网络 → 后端 → 数据库）
4. **记录问题到 TROUBLESHOOTING.md**

### 4. 问题记录规范（重要！）
每次调试后必须在 `TROUBLESHOOTING.md` 中记录：
- ✍️ 问题现象
- 🔍 根本原因
- ✅ 解决方案
- 💡 关键要点
- 📝 提交到 Git

## Technology Stack Standards

### Frontend
- React 18（单 HTML 文件 + CDN）
- Tailwind CSS（原子化 CSS）
- Babel Standalone（浏览器端编译）

### Backend
- Node.js + Express
- MySQL 8.0
- JWT 认证
- bcrypt 加密

### Security
- Helmet：安全 HTTP 头
- CORS：跨域配置（开发环境 `origin: true`）
- 参数化查询：防止 SQL 注入
- HTML 转义：防止 XSS 攻击

## Quality Gates

### 代码提交前检查清单
- [ ] 代码符合 ESLint 规范
- [ ] 关键逻辑有注释
- [ ] 异步操作有错误处理
- [ ] 空数据状态有 UI 提示
- [ ] .gitignore 配置正确
- [ ] 无敏感信息（.env、密码）
- [ ] 提交信息语义清晰
- [ ] 如有调试，已更新 TROUBLESHOOTING.md

### API 开发检查清单
- [ ] 认证中间件已添加
- [ ] 输入参数已验证
- [ ] 错误响应格式统一
- [ ] SQL 使用参数化查询
- [ ] 敏感数据已加密
- [ ] API 已添加到文档

## Governance

本宪章是项目开发的最高准则，所有代码、流程、决策必须遵循本宪章；

违反宪章的代码不得合并；

宪章修订需要：
1. 记录修订原因
2. 更新受影响的文档
3. 通知所有开发者

**Version**: 1.0.0 | **Ratified**: 2025-11-25 | **Last Amended**: 2025-11-25
