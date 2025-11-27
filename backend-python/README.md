# Skill Tracker Backend - Python/FastAPI

多维度技能追踪与成长可视化系统 - Python后端实现

## 🎯 项目简介

这是Skill Tracker的Python后端实现,使用FastAPI框架替代原有的Node.js/Express架构。迁移的主要目的是为后续集成大语言模型(LLM)和RAG功能做准备。

## 🏗️ 技术栈

### 核心框架
- **FastAPI 0.104+** - 高性能异步Web框架
- **SQLAlchemy 2.0+** - 现代化异步ORM
- **Pydantic v2** - 数据验证和设置管理
- **Uvicorn** - ASGI服务器

### 数据库
- **MySQL 8.0+** - 关系型数据库
- **aiomysql** - 异步MySQL驱动
- **Alembic** - 数据库迁移工具

### 安全
- **python-jose** - JWT令牌处理
- **passlib[bcrypt]** - 密码加密
- **bleach** - XSS过滤

### 开发工具
- **pytest** - 测试框架
- **black** - 代码格式化
- **ruff** - 代码检查
- **mypy** - 类型检查
- **loguru** - 日志系统

## 📁 项目结构

```
backend-python/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI应用入口
│   ├── api/                       # API路由层
│   │   ├── __init__.py
│   │   ├── deps.py               # 依赖注入
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py           # 认证接口
│   │       ├── skills.py         # 技能管理接口
│   │       └── activity.py       # 活动日志接口
│   ├── core/                      # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py             # 配置管理
│   │   ├── security.py           # 安全工具
│   │   └── database.py           # 数据库连接
│   ├── models/                    # SQLAlchemy模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── skill_data.py
│   │   └── activity_log.py
│   ├── schemas/                   # Pydantic模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── skill.py
│   │   └── activity.py
│   ├── services/                  # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── skill_service.py
│   │   ├── activity_service.py
│   │   ├── llm/                  # LLM服务(预留)
│   │   └── rag/                  # RAG服务(预留)
│   ├── middleware/                # 中间件
│   │   └── __init__.py
│   └── utils/                     # 工具函数
│       └── __init__.py
├── tests/                         # 测试
│   └── __init__.py
├── scripts/                       # 脚本
├── alembic/                       # 数据库迁移
├── .env.example                   # 环境变量示例
├── requirements.txt               # Python依赖
├── pyproject.toml                 # 项目配置
└── README.md
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.10+
- MySQL 8.0+
- pip 或 Poetry

### 2. 安装依赖

```bash
# 使用pip
pip install -r requirements.txt

# 或使用Poetry(推荐)
poetry install
```

### 3. 配置环境变量

复制`.env.example`为`.env`并修改配置:

```bash
cp .env.example .env
```

编辑`.env`文件:

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=skill_tracker

# JWT配置
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# 服务配置
PORT=8000
DEBUG=True
```

### 4. 运行服务器

```bash
# 开发模式(热重载)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 或直接运行
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

启动后访问:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 📝 API接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 技能管理
- `GET /api/skills` - 获取用户技能数据
- `PUT /api/skills` - 更新技能数据

### 活动日志
- `POST /api/activity` - 记录活动
- `GET /api/activity/heatmap?days=365` - 获取热力图数据

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并查看覆盖率
pytest --cov=app tests/

# 运行特定测试文件
pytest tests/test_auth.py
```

## 🎨 代码质量

```bash
# 代码格式化
black .

# 代码检查
ruff check .

# 类型检查
mypy app/
```

## 🔐 安全特性

- ✅ bcrypt密码加密(与Node.js版本兼容)
- ✅ JWT令牌认证(与Node.js版本兼容)
- ✅ XSS过滤
- ✅ SQL注入防护(ORM参数化查询)
- ✅ CORS跨域配置

## 🤖 LLM集成准备

项目已预留LLM和RAG功能的架构:

- `app/services/llm/` - LLM服务抽象层
- `app/services/rag/` - RAG检索服务层

后续可轻松集成:
- OpenAI API
- Anthropic Claude
- 本地大模型
- 向量数据库(ChromaDB/Qdrant)

## 📊 开发进度

- [x] Phase 1: 环境准备与项目初始化
- [ ] Phase 2: 数据库层实现
- [ ] Phase 3: 安全模块实现
- [ ] Phase 4: Pydantic Schemas定义
- [ ] Phase 5: 认证API实现
- [ ] Phase 6: 技能管理API实现
- [ ] Phase 7: 活动日志API实现
- [ ] Phase 8: 中间件和错误处理
- [ ] Phase 9: LLM架构预留
- [ ] Phase 10: 测试与验证
- [ ] Phase 11: Docker化与部署准备

## 🔄 从Node.js迁移

本项目100%兼容原Node.js后端的API接口:

- API路径保持不变
- 请求/响应格式完全一致
- JWT token互相兼容
- 密码哈希互相兼容
- 前端无需任何修改

## 📖 相关文档

- [功能规格](../specs/003-backend-python-migration/spec.md)
- [实施计划](../specs/003-backend-python-migration/plan.md)
- [任务清单](../specs/003-backend-python-migration/tasks.md)

## 📄 License

MIT

## 👥 Contributors

欢迎贡献代码！
