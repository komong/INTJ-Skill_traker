# 📏 能力刻度尺 - INTJ 技能追踪系统

一个基于 React + Node.js + MySQL 的全栈技能追踪与成长可视化系统，专为 INTJ 人格设计的结构化能力提升工具。

## 🌟 核心功能

### 功能 001 - 核心技能追踪系统
- **多职业角色管理**：支持 AI产品经理、销售等多个职业路径
- **5级技能进阶体系**：从新手到专家的清晰成长路径
- **验收标准勾选**：每个等级都有明确的验收标准
- **练习日志记录**：记录每次练习的心得和感悟
- **数据持久化**：localStorage 本地存储 + MySQL 云端同步

### 功能 002 - 用户认证与可视化仪表盘
- **用户认证系统**：注册/登录，JWT Token 认证（24小时有效期）
- **密码安全**：bcrypt 加密（salt rounds = 12），密码强度验证
- **活动日志自动记录**：勾选标准、写日志时自动记录活动
- **GitHub 风格热力图**：365天活动可视化，5级颜色渐变
- **统计数据展示**：总活跃天数、当前/最长连续打卡、总练习次数
- **本周/本月活动**：实时统计展示

## 🛠️ 技术栈

### 前端
- **React 18**：单 HTML 文件，使用 CDN 加载
- **Tailwind CSS**：原子化 CSS 框架
- **Babel Standalone**：浏览器端 JSX 编译

### 后端
- **Node.js + Express**：RESTful API 服务
- **MySQL 8.0**：关系型数据库
- **JWT**：用户认证（jsonwebtoken）
- **bcrypt**：密码加密
- **Helmet**：安全头设置
- **CORS**：跨域资源共享

### 数据存储
- **MySQL**：云端数据存储
- **localStorage**：本地离线缓存

## 📦 项目结构

```
Skill-traker/
├── backend/                      # 后端代码
│   ├── server.js                # Express 服务器入口
│   ├── .env                     # 环境变量配置（不提交到 Git）
│   ├── package.json             # 后端依赖配置
│   ├── scripts/
│   │   └── init-db.sql         # 数据库初始化脚本
│   ├── src/
│   │   ├── config/
│   │   │   └── db.js           # MySQL 数据库连接配置
│   │   ├── controllers/
│   │   │   ├── authController.js      # 认证控制器
│   │   │   ├── skillController.js     # 技能数据控制器
│   │   │   └── activityController.js  # 活动日志控制器
│   │   ├── routes/
│   │   │   ├── auth.js         # 认证路由
│   │   │   ├── skills.js       # 技能数据路由
│   │   │   └── activity.js     # 活动日志路由
│   │   ├── middleware/
│   │   │   ├── auth.js         # JWT 认证中间件
│   │   │   └── errorHandler.js # 统一错误处理
│   │   └── utils/
│   │       ├── password.js     # 密码加密工具
│   │       ├── response.js     # 统一响应格式
│   │       └── xssFilter.js    # XSS 过滤工具
│   └── test-api.ps1            # API 测试脚本
├── specs/                       # 需求规格文档
│   ├── 001-skill-tracker-core/
│   └── 002-user-auth-dashboard/
├── skill traker.html            # 前端单页应用
├── .gitignore                   # Git 忽略配置
└── README.md                    # 项目说明文档
```

## 🚀 快速开始

### 1. 环境要求

- **Node.js**：v18+ 
- **MySQL**：8.0+
- **npm**：v9+

### 2. 数据库初始化

#### 2.1 启动 MySQL 服务

```powershell
# Windows (管理员权限)
Start-Service MySQL80

# 或手动启动 MySQL 服务
```

#### 2.2 创建数据库

```powershell
cd backend
mysql -u root -p < scripts/init-db.sql
```

这将创建以下表：
- `users` - 用户表
- `user_skill_data` - 技能数据表
- `activity_logs` - 活动日志表
- `db_versions` - 数据库版本表

### 3. 后端配置

#### 3.1 创建环境变量文件

在 `backend/` 目录下创建 `.env` 文件：

```env
# 数据库配置
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=skill_tracker
DB_PORT=3306

# JWT 配置
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=24h

# 服务器配置
PORT=3000
NODE_ENV=development
```

#### 3.2 安装依赖

```bash
cd backend
npm install
```

#### 3.3 启动后端服务

```bash
node server.js
```

服务器将在 `http://localhost:3000` 启动。

### 4. 前端使用

直接在浏览器中打开 `skill traker.html` 文件即可使用。

**注意**：确保后端服务已启动，前端才能正常进行数据同步。

## 📡 API 接口文档

### 认证接口

#### 注册
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "Password123"
}
```

#### 登录
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "Password123"
}
```

#### 验证 Token
```
GET /api/auth/verify
Authorization: Bearer <token>
```

### 技能数据接口

#### 获取技能数据
```
GET /api/skills
Authorization: Bearer <token>
```

#### 保存技能数据
```
PUT /api/skills
Authorization: Bearer <token>
Content-Type: application/json

{
  "skills": [...],
  "version": 1
}
```

### 活动日志接口

#### 记录活动
```
POST /api/activity/log
Authorization: Bearer <token>
Content-Type: application/json

{
  "activityType": "practice_log",
  "skillId": "sales",
  "details": {
    "skillName": "销售能力",
    "level": 1,
    "logContent": "今天的练习心得..."
  }
}
```

#### 获取统计数据
```
GET /api/activity/stats
Authorization: Bearer <token>
```

#### 获取热力图数据
```
GET /api/activity/heatmap?year=2025
Authorization: Bearer <token>
```

## 🔒 安全特性

- **密码加密**：bcrypt（salt rounds = 12）
- **密码强度验证**：至少 8 位，包含大小写字母和数字
- **JWT 认证**：24 小时有效期
- **XSS 过滤**：HTML 转义防止脚本注入
- **SQL 注入防护**：参数化查询
- **CORS 配置**：跨域资源保护
- **Helmet**：安全 HTTP 头

## 🎯 核心概念

### 技能等级体系

每个技能分为 5 个等级，每个等级包含：
- **等级名称**：如"传声筒"、"成交手"等
- **核心目标**：Boss Challenge
- **验收标准**：可勾选的 Checklist
- **专家锦囊**：实用的 Pro Tips
- **练习日志**：记录每次练习

### 热力图算法

活动等级根据每日活动次数计算：
- **Level 0**：无活动（灰色）
- **Level 1**：1-2 次（浅绿）
- **Level 2**：3-5 次（中绿）
- **Level 3**：6-10 次（深绿）
- **Level 4**：>10 次（最深绿）

### 数据同步策略

- **登录时**：从云端同步最新数据
- **修改后**：2 秒防抖后自动同步到云端
- **离线时**：保存到 localStorage
- **冲突处理**：基于版本号检测

## 🧪 测试

### 后端 API 测试

```powershell
cd backend
.\test-api.ps1
```

测试脚本将自动测试所有 API 接口。

## 🤝 贡献指南

### 分支管理

- `main` - 生产环境分支
- `001-skill-tracker-core` - 功能 001 开发分支
- `002-user-auth-dashboard` - 功能 002 开发分支

### 提交规范

使用语义化提交信息：

```
feat: 新功能
fix: 修复 Bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具配置
```

### 开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **开发并测试**
   - 修改代码
   - 本地测试
   - 确保无错误

3. **提交代码**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

4. **推送到远程**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 待实现功能

- [ ] 数据导出/导入（JSON/CSV）
- [ ] 更多图表可视化（折线图、饼图）
- [ ] 移动端响应式优化
- [ ] 目标设定功能（周目标、月目标）
- [ ] 社交分享功能
- [ ] 多语言支持

## 🐛 已知问题

1. **首次登录数据为空**：新用户首次登录时云端无数据，会使用本地初始数据
2. **热力图空白**：新用户没有活动记录时热力图为空，需要先进行一些活动

## 📄 许可证

MIT License

## 👥 作者

- **komong** - [GitHub](https://github.com/komong)

## 🔗 相关链接

- **GitHub 仓库**：https://github.com/komong/INTJ-Skill_traker
- **问题反馈**：https://github.com/komong/INTJ-Skill_traker/issues

---

**💡 温馨提示**：这是一个面向 INTJ 人格的结构化能力提升工具。通过量化和可视化，让能力成长清晰可见！
