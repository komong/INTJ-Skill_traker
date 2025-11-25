# Implementation Plan: 用户认证与可视化仪表盘

**Branch**: `002-user-auth-dashboard` | **Date**: 2025-11-25 | **Spec**: [spec.md](./spec.md)

## Summary

在现有纯前端应用基础上，构建完整的前后端分离架构，实现用户认证、数据云端同步、可视化仪表盘和代码安全防护。采用 Node.js + Express + MySQL 后端，React 前端，JWT Token 认证，实现多设备数据同步和安全防护。

## Technical Context

**后端技术栈**:
- **Language**: Node.js 18+
- **Framework**: Express 4.18+
- **Database**: MySQL 8.0+
- **Authentication**: JWT (jsonwebtoken)
- **Security**: bcrypt, helmet, express-validator
- **ORM**: Sequelize 6.0+ (可选) 或原生 mysql2

**前端技术栈**:
- **Base**: 现有 React 18 单HTML文件
- **HTTP Client**: Fetch API
- **Charts**: React Simple Heatmap (轻量级热力图库)
- **Storage**: localStorage (离线缓存) + API (云端同步)

**部署方案**:
- **后端**: 本地运行或云服务器（阿里云/腾讯云）
- **数据库**: 本地 MySQL 或云数据库
- **前端**: 静态网页托管（GitHub Pages/Vercel）

**安全措施**:
- bcrypt 密码加密 (salt rounds: 12)
- JWT Token 认证 (有效期: 24h)
- Helmet 安全头
- express-validator 输入验证
- CORS 跨域限制
- XSS 过滤
- SQL 注入防护（参数化查询）

---

## Constitution Check

✅ **简洁至上**
- 后端仅实现必要的 API 接口（注册、登录、数据CRUD）
- 前端保持单文件架构，避免过度工程化

✅ **安全优先**
- 密码加密存储
- Token 认证机制
- 输入验证和过滤

✅ **用户体验**
- 离线优先（localStorage缓存）
- 自动同步（联网后自动上传）
- 友好的错误提示

---

## Project Structure

### 后端项目结构

```text
backend/
├── src/
│   ├── config/
│   │   ├── db.js              # MySQL 连接配置
│   │   └── jwt.js             # JWT 密钥配置
│   │
│   ├── middleware/
│   │   ├── auth.js            # JWT 验证中间件
│   │   ├── validator.js       # 输入验证中间件
│   │   └── errorHandler.js   # 统一错误处理
│   │
│   ├── routes/
│   │   ├── auth.js            # 认证路由 (注册/登录)
│   │   ├── skills.js          # 技能数据路由
│   │   └── activity.js        # 活动记录路由
│   │
│   ├── controllers/
│   │   ├── authController.js  # 认证逻辑
│   │   ├── skillController.js # 技能数据逻辑
│   │   └── activityController.js # 活动统计逻辑
│   │
│   ├── models/
│   │   ├── User.js            # 用户模型
│   │   ├── UserSkillData.js   # 技能数据模型
│   │   └── ActivityLog.js     # 活动日志模型
│   │
│   └── utils/
│       ├── password.js        # 密码加密工具
│       ├── xssFilter.js       # XSS 过滤工具
│       └── response.js        # 统一响应格式
│
├── scripts/
│   └── init-db.sql            # 数据库初始化脚本
│
├── .env                       # 环境变量配置
├── server.js                  # 应用入口
└── package.json
```

### 前端改造（在现有 HTML 基础上）

```text
skill traker.html (改造后):
├── 新增组件:
│   ├── LoginPage            # 登录页面
│   ├── RegisterPage         # 注册页面
│   ├── DashboardHome        # 首页仪表盘
│   ├── Heatmap              # 练习热力图
│   ├── StatsCard            # 统计卡片
│   └── SkillList            # 技能列表（优化后）
│
└── 新增工具函数:
    ├── apiClient.js         # API 请求封装
    ├── tokenManager.js      # Token 管理
    └── syncManager.js       # 数据同步逻辑
```

---

## Implementation Phases

### Phase 0: 数据库设计与初始化

**目标**: 设计数据库表结构并初始化

**数据库表设计**:

```sql
-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- 用户技能数据表
CREATE TABLE user_skill_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_data JSON NOT NULL,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    version INT DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- 活动日志表
CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_date DATE NOT NULL,
    activity_count INT DEFAULT 0,
    details JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, activity_date),
    INDEX idx_user_date (user_id, activity_date)
);
```

**验收标准**:
- ✅ 数据库表创建成功
- ✅ 外键关系正确
- ✅ 索引优化完成

---

### Phase 1: 后端 API 基础框架

**目标**: 搭建 Express 服务器和基础中间件

**实现任务**:
1. 初始化 Node.js 项目
   ```bash
   npm init -y
   npm install express mysql2 bcrypt jsonwebtoken dotenv helmet cors express-validator
   npm install --save-dev nodemon
   ```

2. 创建 MySQL 连接池
3. 实现 JWT 认证中间件
4. 实现统一错误处理
5. 配置 CORS 和 Helmet 安全头

**验收标准**:
- ✅ 服务器成功启动在 3000 端口
- ✅ MySQL 连接池正常工作
- ✅ 测试中间件功能正常

---

### Phase 2: 用户认证 API

**目标**: 实现注册、登录、Token验证

**API 设计**:

```javascript
POST /api/auth/register
Body: { username, email, password }
Response: { success: true, token, user: { id, username, email } }

POST /api/auth/login
Body: { username, password }
Response: { success: true, token, user: { id, username, email } }

GET /api/auth/verify
Headers: { Authorization: "Bearer <token>" }
Response: { success: true, user: { id, username, email } }
```

**安全实现**:
- 密码验证：至少8位，包含大小写字母和数字
- bcrypt 加密（salt rounds: 12）
- JWT Token 签名（secret 从环境变量读取）
- Token 有效期 24 小时

**验收标准**:
- ✅ 注册接口返回正确的 Token
- ✅ 密码成功加密存储
- ✅ 登录接口验证密码正确
- ✅ Token 验证中间件正常工作
- ✅ 错误密码返回友好提示

---

### Phase 3: 技能数据 CRUD API

**目标**: 实现技能数据的云端存储和同步

**API 设计**:

```javascript
GET /api/skills
Headers: { Authorization: "Bearer <token>" }
Response: { success: true, data: [...skills] }

PUT /api/skills
Headers: { Authorization: "Bearer <token>" }
Body: { skills: [...], version: 1 }
Response: { success: true, version: 2 }

POST /api/skills/sync
Headers: { Authorization: "Bearer <token>" }
Body: { localData: [...], localVersion: 1 }
Response: { success: true, serverData: [...], serverVersion: 2, action: "merge" }
```

**同步策略**:
- 简单覆盖策略：服务器时间戳最新的数据优先
- 版本号机制：每次更新 version++
- 冲突检测：如果 localVersion < serverVersion，提示用户

**验收标准**:
- ✅ 用户只能访问自己的数据
- ✅ 数据保存到 JSON 字段成功
- ✅ 同步接口正确处理冲突
- ✅ SQL 注入测试通过

---

### Phase 4: 活动日志与热力图数据

**目标**: 记录用户每日活跃度，生成热力图数据

**API 设计**:

```javascript
POST /api/activity/log
Headers: { Authorization: "Bearer <token>" }
Body: { date: "2025-11-25", activityType: "log_added", skillId: "ai-agent" }
Response: { success: true }

GET /api/activity/heatmap?year=2025
Headers: { Authorization: "Bearer <token>" }
Response: { 
  success: true, 
  data: [
    { date: "2025-11-25", count: 5, level: 3 },
    { date: "2025-11-24", count: 2, level: 1 }
  ]
}

GET /api/activity/stats
Headers: { Authorization: "Bearer <token>" }
Response: {
  success: true,
  totalDays: 120,
  longestStreak: 15,
  currentStreak: 7,
  totalLogs: 350
}
```

**验收标准**:
- ✅ 每次添加日志时自动记录活动
- ✅ 热力图数据覆盖365天
- ✅ level 计算正确（0-4，基于 count）
- ✅ 统计数据准确

---

### Phase 5: 前端认证功能集成

**目标**: 在现有 HTML 上添加登录/注册页面

**实现任务**:
1. 创建 LoginPage 和 RegisterPage 组件
2. 实现 Token 管理（存储在 localStorage）
3. 实现 API 请求拦截器（自动添加 Token）
4. 实现登录状态管理
5. 实现自动登录（Token 有效时）

**关键代码**:

```javascript
// Token 管理
const tokenManager = {
  getToken: () => localStorage.getItem('authToken'),
  setToken: (token) => localStorage.setItem('authToken', token),
  clearToken: () => localStorage.removeItem('authToken'),
  isValid: () => {
    const token = tokenManager.getToken();
    if (!token) return false;
    // 简单验证（生产环境应验证过期时间）
    return true;
  }
};

// API 请求封装
const apiClient = {
  async request(url, options = {}) {
    const token = tokenManager.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    };
    
    const response = await fetch(`http://localhost:3000${url}`, {
      ...options,
      headers
    });
    
    if (response.status === 401) {
      tokenManager.clearToken();
      window.location.reload();
    }
    
    return response.json();
  }
};
```

**验收标准**:
- ✅ 未登录时显示登录页
- ✅ 注册成功后自动登录
- ✅ Token 过期时自动跳转登录页
- ✅ 密码输入时显示强度提示
- ✅ 错误信息友好展示

---

### Phase 6: 首页仪表盘实现

**目标**: 实现可视化首页，包含热力图和统计数据

**实现任务**:
1. 创建 DashboardHome 组件
2. 集成热力图组件（使用轻量级库或自己实现）
3. 实现统计卡片（总完成度、连续打卡天数、本周活跃度）
4. 实现最近活动列表
5. 实现"当前攻克中"技能卡片

**热力图实现**（简化版 SVG）:

```javascript
function Heatmap({ data }) {
  const weeks = 52;
  const cellSize = 12;
  const gap = 2;
  
  const getLevel = (count) => {
    if (count === 0) return 0;
    if (count <= 2) return 1;
    if (count <= 5) return 2;
    if (count <= 10) return 3;
    return 4;
  };
  
  const colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'];
  
  return (
    <svg width={weeks * (cellSize + gap)} height={7 * (cellSize + gap)}>
      {data.map((day, i) => {
        const week = Math.floor(i / 7);
        const dayOfWeek = i % 7;
        const level = getLevel(day.count);
        
        return (
          <rect
            key={i}
            x={week * (cellSize + gap)}
            y={dayOfWeek * (cellSize + gap)}
            width={cellSize}
            height={cellSize}
            fill={colors[level]}
            rx={2}
            title={`${day.date}: ${day.count} activities`}
          />
        );
      })}
    </svg>
  );
}
```

**验收标准**:
- ✅ 热力图正确显示365天数据
- ✅ 点击日期显示详情
- ✅ 统计数据实时更新
- ✅ 响应式布局适配移动端

---

### Phase 7: UI优化 - 职业与技能分离

**目标**: 优化信息架构，职业页不显示等级

**实现任务**:
1. 修改职业角色页：只显示技能卡片列表
2. 技能卡片显示：
   - 技能图标和名称
   - 整体完成度进度条
   - 当前等级徽章
   - 最后练习时间
3. 点击技能卡片进入详情页（显示5级体系）
4. 添加面包屑导航（首页 → 职业 → 技能 → 等级详情）

**验收标准**:
- ✅ 职业页不显示等级信息
- ✅ 技能卡片信息完整
- ✅ 导航层级清晰
- ✅ 移动端体验良好

---

### Phase 8: 数据同步与离线支持

**目标**: 实现智能数据同步，支持离线使用

**同步逻辑**:

```javascript
const syncManager = {
  async sync() {
    const localData = JSON.parse(localStorage.getItem('skillTrackerData'));
    const localVersion = parseInt(localStorage.getItem('dataVersion') || '0');
    
    try {
      const response = await apiClient.request('/api/skills/sync', {
        method: 'POST',
        body: JSON.stringify({ localData, localVersion })
      });
      
      if (response.action === 'update') {
        localStorage.setItem('skillTrackerData', JSON.stringify(response.serverData));
        localStorage.setItem('dataVersion', response.serverVersion);
      }
    } catch (error) {
      console.warn('同步失败，使用离线模式', error);
    }
  },
  
  startAutoSync() {
    setInterval(() => this.sync(), 60000); // 每分钟同步一次
  }
};
```

**验收标准**:
- ✅ 离线时数据仍保存在 localStorage
- ✅ 联网后自动同步到服务器
- ✅ 多设备数据保持一致
- ✅ 同步失败有友好提示

---

### Phase 9: 数据导出与导入

**目标**: 实现数据备份功能

**实现任务**:
1. 导出按钮：下载 JSON 文件
2. 导入按钮：上传 JSON 文件并验证
3. 数据格式验证
4. 导入后同步到服务器

**验收标准**:
- ✅ 导出文件包含完整数据
- ✅ 导入成功恢复数据
- ✅ 格式错误时友好提示

---

## Testing Strategy

### 安全测试
1. **XSS 测试**: 在日志中输入 `<script>alert(1)</script>`
2. **SQL 注入测试**: 在登录表单输入 `' OR '1'='1`
3. **JWT 测试**: 使用伪造的 Token 访问 API
4. **密码强度测试**: 尝试弱密码注册

### 功能测试
1. **注册登录**: 完整流程测试
2. **数据同步**: 多设备测试
3. **热力图**: 365天数据渲染测试
4. **离线模式**: 断网后操作测试

---

## Risk Mitigation

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| MySQL 连接失败 | 高 | 实现连接池重试机制，提供友好错误提示 |
| Token 泄露 | 高 | 设置合理的过期时间，使用 HTTPS |
| 数据同步冲突 | 中 | 简单覆盖策略，后期实现合并算法 |
| 热力图性能问题 | 低 | 使用虚拟滚动，按需加载数据 |

---

## Dependencies

### 后端依赖

```json
{
  "express": "^4.18.0",
  "mysql2": "^3.6.0",
  "bcrypt": "^5.1.0",
  "jsonwebtoken": "^9.0.0",
  "dotenv": "^16.3.0",
  "helmet": "^7.1.0",
  "cors": "^2.8.5",
  "express-validator": "^7.0.0"
}
```

### 前端无需额外依赖
- 保持单 HTML 文件
- 热力图使用原生 SVG 实现

---

## Deployment

### 后端部署

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 MySQL 配置和 JWT Secret

# 2. 初始化数据库
mysql -u root -p < scripts/init-db.sql

# 3. 启动服务
npm start
```

### 前端部署
- 直接打开 HTML 文件
- 或托管到 GitHub Pages / Vercel

---

## Success Metrics

- ✅ 所有 24 个 FR 实现
- ✅ 通过 OWASP Top 10 基础检测
- ✅ 热力图渲染时间 < 1s
- ✅ API 响应时间 < 500ms
- ✅ 用户注册到首次使用 < 3分钟

---

## Next Steps

1. **立即执行**: Phase 0 - 设计并初始化数据库
2. **后续执行**: Phase 1-2 - 搭建后端 API
3. **最后生成**: 使用 `/specify tasks` 生成详细任务分解

---

**版本**: 1.0.0 | **最后更新**: 2025-11-25
