# Implementation Plan: 后端架构迁移至Python

**Feature**: `003-backend-python-migration`  
**Timeline**: 9-12天  
**Priority**: High

## Overview

将后端从Node.js/Express迁移到Python/FastAPI，为后续集成大语言模型（LLM）和RAG功能做准备。迁移过程中保持API接口不变，确保前端应用无需修改即可正常工作。

## Goals

1. **完整功能迁移**: 所有现有API接口（认证、技能管理、活动日志）100%迁移
2. **零前端改动**: 保持API请求/响应格式完全一致，前端无需修改
3. **安全兼容性**: JWT token和bcrypt密码哈希与Node.js版本兼容
4. **架构预留**: 为LLM和RAG功能预留清晰的服务层和接口
5. **现代化架构**: 采用Python生态最佳实践（FastAPI、SQLAlchemy 2.0、Pydantic v2）

## Non-Goals

- 修改数据库表结构（使用现有MySQL schema）
- 实现具体的LLM功能（本次只做架构预留）
- 修改前端代码
- 改变API接口路径或响应格式

## Phases

### Phase 1: 环境准备与项目初始化（Day 1）

**目标**: 建立Python后端项目的基础架构

**任务**:
1. 创建 `backend-python` 目录结构
2. 初始化Poetry项目 (`poetry init`)
3. 添加核心依赖:
   - FastAPI (Web框架)
   - SQLAlchemy 2.0+ (ORM)
   - Pydantic v2 (数据验证)
   - aiomysql/asyncmy (异步MySQL驱动)
   - python-jose (JWT)
   - passlib[bcrypt] (密码加密)
   - uvicorn (ASGI服务器)
4. 配置开发工具:
   - pytest (测试框架)
   - black (代码格式化)
   - ruff (代码检查)
   - mypy (类型检查)
5. 创建 `.env.example` 配置模板
6. 设置 `pyproject.toml` 项目配置
7. 创建基础目录结构（app/api、app/models、app/services等）

**验收标准**:
- [ ] 项目目录结构完整
- [ ] `poetry install` 成功执行
- [ ] 可以运行 `uvicorn app.main:app --reload`
- [ ] 访问 `http://localhost:8000/docs` 可以看到API文档

---

### Phase 2: 数据库层实现（Day 2-3）

**目标**: 实现与现有MySQL数据库的连接和ORM模型映射

**任务**:
1. **数据库连接配置** (`app/core/database.py`):
   - 创建异步数据库引擎
   - 配置连接池（与Node.js版本参数对齐）
   - 实现SessionLocal工厂函数
   - 创建 `get_db()` 依赖注入函数

2. **SQLAlchemy模型定义**:
   - `app/models/user.py`: User模型（映射users表）
   - `app/models/skill_data.py`: UserSkillData模型
   - `app/models/activity_log.py`: ActivityLog模型
   - 使用 `Mapped` 类型注解（SQLAlchemy 2.0风格）
   - 定义模型关系（User -> UserSkillData, User -> ActivityLog）

3. **Alembic配置**:
   - 初始化Alembic (`alembic init alembic`)
   - 配置 `alembic/env.py` 连接数据库
   - 创建初始迁移（检测现有表结构）
   - 验证迁移脚本不会修改现有表

4. **数据库测试脚本** (`scripts/test_db.py`):
   - 测试数据库连接
   - 测试模型CRUD操作
   - 验证JSON字段序列化

**验收标准**:
- [ ] 成功连接到现有MySQL数据库
- [ ] SQLAlchemy模型定义与现有表结构完全匹配
- [ ] 可以正常读取现有测试用户数据
- [ ] JSON字段（skill_data、details）序列化正确
- [ ] Alembic迁移脚本生成成功（无实际变更）

---

### Phase 3: 安全模块实现（Day 3-4）

**目标**: 实现与Node.js版本兼容的安全机制

**任务**:
1. **密码加密** (`app/core/security.py`):
   - 实现 `hash_password(password: str) -> str`
   - 实现 `verify_password(plain_password: str, hashed: str) -> bool`
   - 使用bcrypt，确保与Node.js版本兼容（相同的salt rounds）
   - 编写测试验证与Node.js bcrypt哈希的兼容性

2. **JWT处理**:
   - 实现 `create_access_token(data: dict) -> str`
   - 实现 `decode_access_token(token: str) -> dict`
   - 使用与Node.js相同的JWT密钥和算法（HS256）
   - 设置相同的过期时间（24小时）

3. **认证依赖** (`app/api/deps.py`):
   - 实现 `get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User`
   - 从Authorization header提取token
   - 验证token有效性
   - 从数据库加载用户信息

4. **XSS过滤** (`app/utils/xss_filter.py`):
   - 使用bleach库清理用户输入
   - 实现 `sanitize_html(text: str) -> str`
   - 在日志和描述字段应用过滤

5. **安全测试**:
   - 测试Node.js创建的用户能否在Python后端登录
   - 测试Node.js生成的JWT token是否能被Python验证
   - 测试XSS注入攻击防护

**验收标准**:
- [ ] 可以验证Node.js版本创建的用户密码
- [ ] 可以验证Node.js版本生成的JWT token
- [ ] Python生成的token可以被Node.js验证（交叉测试）
- [ ] XSS攻击代码被正确过滤

---

### Phase 4: Pydantic Schemas定义（Day 4）

**目标**: 定义API的请求和响应数据模型

**任务**:
1. **用户相关schemas** (`app/schemas/user.py`):
   - `UserRegister`: 注册请求（username, email, password）
   - `UserLogin`: 登录请求（username_or_email, password）
   - `UserOut`: 用户信息响应（不包含密码）
   - `TokenResponse`: Token响应

2. **技能相关schemas** (`app/schemas/skill.py`):
   - `SkillDataOut`: 技能数据响应
   - `SkillDataUpdate`: 技能数据更新请求
   - `SkillDataResponse`: 带版本号的响应

3. **活动相关schemas** (`app/schemas/activity.py`):
   - `ActivityCreate`: 活动记录创建
   - `ActivityOut`: 活动响应
   - `HeatmapData`: 热力图数据点
   - `HeatmapResponse`: 热力图响应

4. **通用响应格式** (`app/schemas/common.py`):
   - `SuccessResponse[T]`: 成功响应包装器
   - `ErrorResponse`: 错误响应
   - `ErrorDetail`: 错误详情

**验收标准**:
- [ ] 所有schemas有完整的类型注解
- [ ] 包含数据验证规则（长度、格式、必填等）
- [ ] 响应格式与Node.js版本完全一致
- [ ] API文档自动显示正确的请求/响应示例

---

### Phase 5: 认证API实现（Day 5-6）

**目标**: 实现用户注册和登录功能

**任务**:
1. **认证服务** (`app/services/auth_service.py`):
   - `async def register_user(user_data: UserRegister, db: Session) -> User`
   - `async def authenticate_user(username_or_email: str, password: str, db: Session) -> User | None`
   - `async def get_user_by_id(user_id: int, db: Session) -> User | None`

2. **认证路由** (`app/api/v1/auth.py`):
   - `POST /api/auth/register`: 用户注册
   - `POST /api/auth/login`: 用户登录
   - `GET /api/auth/me`: 获取当前用户信息
   - 统一错误处理

3. **密码强度验证**:
   - 在Pydantic schema中添加正则验证
   - 至少8位，包含大小写字母和数字

4. **响应格式统一** (`app/utils/response.py`):
   - `success_response(data, message="Success")`
   - `error_response(code, message, details=None)`

5. **单元测试** (`tests/test_auth.py`):
   - 测试注册流程
   - 测试登录成功/失败
   - 测试JWT token生成和验证
   - 测试密码强度校验

**验收标准**:
- [ ] 注册接口返回正确的JWT token和用户信息
- [ ] 登录接口验证用户名或邮箱
- [ ] 错误响应格式与Node.js版本一致
- [ ] 单元测试覆盖率 > 80%
- [ ] 可以使用Postman/curl测试成功

---

### Phase 6: 技能管理API实现（Day 6-7）

**目标**: 实现技能数据的读取和更新功能

**任务**:
1. **技能服务** (`app/services/skill_service.py`):
   - `async def get_user_skills(user_id: int, db: Session) -> dict`
   - `async def update_user_skills(user_id: int, skill_data: dict, version: int, db: Session) -> UserSkillData`
   - 实现版本冲突检测（乐观锁）

2. **技能路由** (`app/api/v1/skills.py`):
   - `GET /api/skills`: 获取当前用户的技能数据
   - `PUT /api/skills`: 更新技能数据
   - 需要JWT认证（使用 `get_current_user` 依赖）

3. **JSON序列化优化**:
   - 确保复杂的嵌套JSON正确处理
   - 处理日期时间格式（ISO 8601）

4. **单元测试** (`tests/test_skills.py`):
   - 测试获取技能数据
   - 测试更新技能数据
   - 测试版本冲突检测
   - 测试未授权访问

**验收标准**:
- [ ] 可以读取和更新完整的技能JSON数据
- [ ] 版本冲突时返回409错误
- [ ] 用户只能访问自己的数据
- [ ] 响应格式与Node.js版本一致

---

### Phase 7: 活动日志API实现（Day 7-8）

**目标**: 实现活动记录和热力图数据生成

**任务**:
1. **活动服务** (`app/services/activity_service.py`):
   - `async def record_activity(user_id: int, details: dict, db: Session) -> ActivityLog`
   - `async def get_heatmap_data(user_id: int, days: int, db: Session) -> list[dict]`
   - 实现日期聚合逻辑（同一天的活动累加）

2. **活动路由** (`app/api/v1/activity.py`):
   - `POST /api/activity`: 记录活动
   - `GET /api/activity/heatmap?days=365`: 获取热力图数据
   - 需要JWT认证

3. **热力图数据格式**:
   ```json
   [
     { "date": "2025-11-25", "count": 5, "level": 3 },
     { "date": "2025-11-24", "count": 2, "level": 1 }
   ]
   ```

4. **单元测试** (`tests/test_activity.py`):
   - 测试记录活动
   - 测试热力图数据生成
   - 测试日期范围过滤

**验收标准**:
- [ ] 活动记录正确保存到数据库
- [ ] 热力图数据格式正确
- [ ] 同一天多次活动正确累加
- [ ] 日期范围查询正确

---

### Phase 8: 中间件和错误处理（Day 8）

**目标**: 实现统一的中间件和错误处理机制

**任务**:
1. **CORS中间件** (`app/middleware/cors_middleware.py`):
   - 配置与Node.js版本相同的CORS策略
   - 允许所有来源（开发模式）
   - 配置允许的方法和头

2. **日志中间件** (`app/middleware/logging_middleware.py`):
   - 记录每个请求的方法、路径、耗时
   - 使用loguru结构化日志

3. **全局异常处理** (`app/main.py`):
   - 捕获所有未处理的异常
   - 返回统一的错误响应格式
   - 记录详细的错误日志

4. **健康检查接口**:
   - `GET /health`: 返回服务状态和数据库连接状态

**验收标准**:
- [ ] 前端可以正常跨域请求
- [ ] 所有请求都有日志记录
- [ ] 异常错误返回友好的错误信息
- [ ] `/health` 接口返回正确的状态

---

### Phase 9: LLM架构预留（Day 9-10）

**目标**: 为后续LLM功能预留清晰的服务层架构

**任务**:
1. **LLM服务抽象** (`app/services/llm/base.py`):
   - 定义 `LLMProvider` 抽象基类
   - 定义统一的接口：`generate()`, `embed()`

2. **OpenAI提供商** (`app/services/llm/openai_provider.py`):
   - 实现OpenAI API调用（示例）
   - 配置API密钥和模型参数

3. **Claude提供商** (`app/services/llm/claude_provider.py`):
   - 实现Anthropic API调用（示例）

4. **技能推荐服务** (`app/services/llm/skill_recommendation.py`):
   - 定义推荐服务接口（暂不实现）
   - 设计上下文构建逻辑

5. **RAG架构** (`app/services/rag/`):
   - 定义向量存储接口 (`vector_store.py`)
   - 定义检索服务接口 (`retriever.py`)

6. **配置更新** (`app/core/config.py`):
   - 添加LLM相关配置项（API密钥、模型名称等）

**验收标准**:
- [ ] LLM服务抽象接口定义清晰
- [ ] 至少实现一个示例LLM调用（OpenAI）
- [ ] RAG架构目录结构完整
- [ ] 配置项支持多个LLM提供商

---

### Phase 10: 测试与验证（Day 10-11）

**目标**: 全面测试API兼容性和性能

**任务**:
1. **API兼容性测试**:
   - 将Node.js的 `test-api.ps1` 改为指向Python后端
   - 验证所有接口响应格式一致
   - 测试跨版本兼容性（Node.js token → Python验证）

2. **集成测试**:
   - 端到端测试注册→登录→更新技能→查看热力图流程
   - 测试并发请求

3. **性能测试**:
   - 使用locust或ab进行压力测试
   - 验证响应时间 < 200ms
   - 测试100并发用户场景

4. **安全测试**:
   - XSS注入测试
   - SQL注入测试（尝试绕过ORM）
   - JWT token过期测试
   - 未授权访问测试

5. **代码质量检查**:
   - 运行 `black .` 格式化代码
   - 运行 `ruff check .` 检查代码规范
   - 运行 `mypy .` 类型检查
   - 查看测试覆盖率报告

**验收标准**:
- [ ] 所有API测试用例通过
- [ ] 性能达标（响应时间 < 200ms）
- [ ] 测试覆盖率 > 80%
- [ ] 无代码质量警告

---

### Phase 11: Docker化与部署准备（Day 11-12）

**目标**: 提供完整的容器化和部署方案

**任务**:
1. **Dockerfile**:
   - 使用多阶段构建优化镜像大小
   - 基础镜像：`python:3.11-slim`
   - 安装Poetry和依赖
   - 暴露8000端口

2. **docker-compose.yml**:
   - 定义Python后端服务
   - 定义MySQL数据库服务
   - 配置网络和卷

3. **环境变量配置**:
   - 创建 `.env.example`
   - 文档说明所有配置项

4. **数据迁移脚本** (`scripts/migrate_from_nodejs.py`):
   - 验证数据库数据完整性
   - 提供数据清洗工具（如有必要）

5. **部署文档** (`README.md`):
   - 本地开发环境搭建
   - Docker部署步骤
   - 生产环境配置建议
   - 从Node.js迁移指南

**验收标准**:
- [ ] `docker-compose up` 可以启动完整服务
- [ ] 容器内API正常工作
- [ ] 部署文档清晰完整
- [ ] 提供从Node.js迁移的详细步骤

---

## Risk Mitigation

### 风险1: JWT和bcrypt兼容性问题
**影响**: 现有用户无法登录，前端token失效  
**缓解措施**:
- 在Phase 3优先测试兼容性
- 使用相同的密钥、算法、salt rounds
- 编写交叉验证测试
- 如有问题，考虑实现双验证机制（同时支持两种格式）

### 风险2: API响应格式不一致
**影响**: 前端报错，需要修改前端代码  
**缓解措施**:
- 在Phase 4严格定义响应格式
- 使用Pydantic确保字段类型一致
- 编写API对比测试工具
- 保留Node.js版本作为参考

### 风险3: 性能下降
**影响**: 用户体验变差  
**缓解措施**:
- 在Phase 10进行性能测试
- 使用异步I/O和连接池
- 必要时使用缓存（Redis）
- 数据库查询优化

### 风险4: 数据库兼容性问题
**影响**: 数据读写错误  
**缓解措施**:
- 在Phase 2仔细映射表结构
- 使用Alembic验证迁移
- 测试JSON字段序列化
- 备份数据库后再测试

## Dependencies

**外部依赖**:
- MySQL 8.0+ 已安装并运行
- Python 3.10+ 环境
- 现有的Node.js后端和数据库（用于对比测试）

**内部依赖**:
- 需要002功能的数据库表结构
- 需要前端应用进行集成测试

## Success Metrics

1. **功能完整性**: 100%的现有API迁移成功
2. **兼容性**: 前端零修改即可工作
3. **性能**: API响应时间 < 200ms
4. **安全性**: 通过OWASP Top 10检测
5. **代码质量**: 测试覆盖率 > 80%
6. **架构扩展性**: LLM服务接口定义清晰，易于扩展

## Timeline

```
Day 1:   Phase 1 - 环境准备
Day 2-3: Phase 2 - 数据库层
Day 3-4: Phase 3 - 安全模块
Day 4:   Phase 4 - Pydantic Schemas
Day 5-6: Phase 5 - 认证API
Day 6-7: Phase 6 - 技能管理API
Day 7-8: Phase 7 - 活动日志API
Day 8:   Phase 8 - 中间件和错误处理
Day 9-10: Phase 9 - LLM架构预留
Day 10-11: Phase 10 - 测试与验证
Day 11-12: Phase 11 - Docker化与部署
```

**总计**: 9-12个工作日

## Notes

- 优先保证功能完整性和兼容性，性能优化可以后续迭代
- LLM功能在本次只做架构预留，不实现具体调用
- 保留Node.js版本作为备份，直到Python版本稳定运行
- 使用feature branch开发，主分支保持Node.js版本
