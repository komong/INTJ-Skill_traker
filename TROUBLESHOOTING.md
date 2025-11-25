# Troubleshooting Guide - 实践手册

本文档记录开发过程中遇到的问题及解决方案，供后续参考。

## 📅 2025-11-25 调试记录

### 1. CORS 跨域问题

**问题描述**：
前端（file:// 协议）无法连接到后端 API，浏览器提示 "Failed to fetch"

**原因分析**：
- 初始 CORS 配置使用 `origin: '*'` 但 `credentials: false`
- 从本地 HTML 文件访问时，浏览器有更严格的 CORS 限制

**解决方案**：
```javascript
// backend/server.js
app.use(cors({
    origin: true,  // 允许所有来源并返回请求的 origin
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true  // 允许携带凭证
}));
```

**关键要点**：
- 开发环境使用 `origin: true` 而不是 `origin: '*'`
- 必须设置 `credentials: true` 才能携带 Token
- 生产环境建议配置具体的允许域名

---

### 2. Token 认证循环问题

**问题描述**：
用户登录后立即提示"认证已过期，请重新登录"，陷入登录循环

**原因分析**：
- API 请求拦截器在 401 错误时立即执行 `window.location.reload()`
- 导致刚登录的用户也被强制刷新页面，Token 丢失

**解决方案**：
```javascript
// 修改前（错误）
if (response.status === 401) {
    tokenManager.clearToken();
    window.location.reload();  // ❌ 不要立即刷新
    throw new Error('认证已过期，请重新登录');
}

// 修改后（正确）
if (response.status === 401) {
    throw new Error('Token 过期，请重新登录');  // ✅ 抛出错误让上层处理
}
```

**关键要点**：
- 不要在全局拦截器中执行 `window.location.reload()`
- 让每个调用处自行决定如何处理 401 错误
- Token 验证失败时，由 `checkAuth()` 统一清除状态

---

### 3. 数据加载空白页面问题

**问题描述**：
登录成功后页面显示空白，浏览器控制台无明显错误

**原因分析**：
- 仪表盘组件加载热力图数据时，后端返回空数组
- 未对空数据进行容错处理，导致 React 渲染失败

**解决方案**：
```javascript
// 添加安全访问和默认值
setHeatmapData(heatmapRes.data?.heatmap || []);
setStats(statsRes.data || {});

// 添加空数据提示
{weeklyData.length > 0 ? (
    // 渲染热力图
) : (
    <div className="w-full text-center py-12 text-slate-400">
        <div className="text-5xl mb-3">📊</div>
        <p>还没有活动记录，开始你的第一次练习吧！</p>
    </div>
)}
```

**关键要点**：
- 使用可选链操作符 `?.` 和默认值 `||` 进行防御性编程
- 空数据状态需要显式的 UI 提示
- 在 catch 块中也要设置默认值，避免组件崩溃

---

### 4. Git 推送连接失败

**问题描述**：
使用 HTTPS 协议推送到 GitHub 时，报错 "Failed to connect to github.com port 443"

**原因分析**：
- 网络环境对 HTTPS 443 端口有限制
- 可能是防火墙、代理或网络配置问题

**解决方案**：
```bash
# 改用 SSH 协议
git remote set-url origin git@github.com:komong/INTJ-Skill_traker.git
git push -u origin 001-skill-tracker-core
```

**关键要点**：
- SSH 协议通常比 HTTPS 更稳定
- 需要事先配置 SSH 密钥
- 如果 SSH 也失败，检查网络代理设置

---

### 5. node_modules 被误提交

**问题描述**：
执行 `git status` 时发现大量 node_modules 文件准备提交

**原因分析**：
- 项目初始化时未创建 .gitignore 文件
- npm install 后所有依赖都被 Git 追踪

**解决方案**：
```bash
# 1. 创建 .gitignore
# 2. 从 Git 追踪中移除（但保留本地文件）
git rm -r --cached backend/node_modules

# 3. 重新添加并提交
git add .
git commit -m "chore: 添加 .gitignore，移除 node_modules"
```

**关键要点**：
- 项目初始化时第一件事就是创建 .gitignore
- 使用 `--cached` 参数只移除 Git 追踪，不删除本地文件
- .gitignore 应包含：node_modules/、.env、logs/ 等

---

### 6. 环境变量配置问题

**问题描述**：
后端启动时报错 "JWT_SECRET is not defined"

**原因分析**：
- .env 文件未创建或未正确加载
- 环境变量命名或路径配置错误

**解决方案**：
```javascript
// 确保在文件顶部加载
import dotenv from 'dotenv';
dotenv.config();

// 验证必要的环境变量
if (!process.env.JWT_SECRET) {
    throw new Error('JWT_SECRET must be defined in .env file');
}
```

**关键要点**：
- .env 文件不应提交到 Git（添加到 .gitignore）
- README.md 中提供 .env.example 示例
- 启动时验证关键环境变量是否存在

---

### 7. MySQL 服务未启动

**问题描述**：
后端启动时报错 "Can't connect to MySQL server on 'localhost:3306'"

**原因分析**：
- MySQL 服务处于停止状态
- 需要手动启动服务

**解决方案**：
```powershell
# Windows - 管理员权限
Start-Service MySQL80

# 或检查服务状态
Get-Service MySQL80

# 设置自动启动
Set-Service -Name MySQL80 -StartupType Automatic
```

**关键要点**：
- 开发前检查依赖服务是否启动
- 考虑将 MySQL 设置为自动启动
- 添加数据库连接错误的友好提示

---

## 🎯 最佳实践总结

### 调试流程

1. **查看浏览器控制台**
   - Console：查看错误日志和 API 响应
   - Network：检查请求状态和返回数据
   - Application：查看 localStorage 和 Cookie

2. **检查后端日志**
   - 服务器启动日志
   - API 请求日志
   - 数据库连接状态

3. **分层排查**
   - 前端 → 网络 → 后端 → 数据库
   - 逐层确认每个环节是否正常

### 防御性编程

```javascript
// ✅ 好的实践
const data = response.data?.items || [];
const user = tokenManager.getUser();
if (!user) return;

// ❌ 避免的写法
const data = response.data.items;  // 可能 undefined
const user = tokenManager.getUser();
user.name  // 直接使用可能报错
```

### 错误处理

```javascript
// ✅ 完整的错误处理
try {
    const result = await apiCall();
    return result;
} catch (err) {
    console.error('操作失败:', err);
    // 设置默认值或显示错误 UI
    setData([]);
    setError(err.message);
} finally {
    setLoading(false);
}
```

### Git 工作流

```bash
# 1. 开发前先拉取最新代码
git pull origin main

# 2. 创建功能分支
git checkout -b feature/new-feature

# 3. 提交前检查状态
git status

# 4. 分步提交
git add <specific-files>
git commit -m "feat: 描述"

# 5. 推送前确保 .gitignore 正确
```

---

## 📋 调试检查清单

每次遇到问题时，按此清单逐项检查：

- [ ] 浏览器控制台是否有错误？
- [ ] Network 标签中 API 请求状态如何？
- [ ] 后端服务是否正常运行？
- [ ] MySQL 服务是否启动？
- [ ] .env 环境变量是否配置？
- [ ] CORS 配置是否正确？
- [ ] Token 是否存在且有效？
- [ ] 数据结构是否添加了安全访问？
- [ ] 空数据状态是否有 UI 提示？
- [ ] Git 提交前是否检查了 .gitignore？

---

## 🔄 持续更新

本文档会随着开发过程持续更新，记录新遇到的问题和解决方案。每次调试后都应该：

1. ✍️ 记录问题现象
2. 🔍 分析根本原因
3. ✅ 记录解决方案
4. 💡 总结关键要点
5. 📝 提交到 Git

---

**最后更新时间**：2025-11-25  
**维护者**：komong
