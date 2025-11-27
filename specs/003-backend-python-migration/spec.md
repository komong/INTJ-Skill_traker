# Feature Specification: 后端架构迁移至Python

**Feature Branch**: `003-backend-python-migration`  
**Created**: 2025-11-26  
**Status**: Draft  
**Input**: 用户需求：将后端从Node.js/Express迁移到Python框架，为后续集成LLM和RAG做准备

## User Scenarios & Testing *(mandatory)*

### User Story 1 - API功能完整迁移 (Priority: P1)

作为一名系统维护者，我希望将现有的所有API接口从Node.js迁移到Python后端，确保前端应用无需修改即可正常工作，以便为后续AI功能集成做好准备。

**Why this priority**: API功能完整性是后端迁移的基础，必须保证与现有前端的完全兼容。

**Independent Test**: 可以通过运行现有的API测试脚本，验证所有接口的请求和响应格式保持一致。

**Acceptance Scenarios**:

1. **Given** Python后端启动, **When** 前端发送 `POST /api/auth/register` 请求, **Then** 返回与Node.js版本相同格式的响应（包含JWT token、用户信息）
2. **Given** 用户已登录, **When** 前端发送 `GET /api/skills` 请求（带Authorization header）, **Then** 返回用户的技能数据
3. **Given** 用户更新技能数据, **When** 前端发送 `PUT /api/skills` 请求, **Then** 数据正确保存到MySQL并返回成功响应
4. **Given** 用户添加活动日志, **When** 前端发送 `POST /api/activity` 请求, **Then** 活动记录保存并更新热力图数据
5. **Given** 用户请求热力图数据, **When** 前端发送 `GET /api/activity/heatmap?days=365`, **Then** 返回过去365天的活动统计

---

### User Story 2 - Python现代化项目结构 (Priority: P1)

作为开发者，我希望Python后端采用现代化的项目结构和最佳实践，以便项目具有良好的可维护性和扩展性。

**Why this priority**: 良好的项目结构是后续开发的基础。

**Independent Test**: 可以通过检查项目目录结构、代码组织、配置管理来验证。

**Acceptance Scenarios**:

1. **Given** 项目采用FastAPI框架, **When** 查看项目结构, **Then** 包含 `app/api`、`app/models`、`app/services`、`app/core` 等标准目录
2. **Given** 使用Poetry管理依赖, **When** 执行 `poetry install`, **Then** 自动安装所有依赖并创建虚拟环境
3. **Given** 采用环境变量配置, **When** 启动应用, **Then** 从 `.env` 文件加载配置（数据库连接、JWT密钥等）
4. **Given** 使用Pydantic进行数据验证, **When** API接收到错误格式的数据, **Then** 返回清晰的验证错误信息
5. **Given** 使用SQLAlchemy ORM, **When** 执行数据库操作, **Then** 使用异步查询和连接池

---

### User Story 3 - 完整的安全机制迁移 (Priority: P1)

作为安全工程师，我希望Python后端实现与Node.js版本相同的安全机制，包括密码加密、JWT认证、XSS防护、SQL注入防护等。

**Why this priority**: 安全是应用的基石，必须在迁移时完整保留。

**Independent Test**: 可以通过安全测试工具和手动测试验证各项安全措施。

**Acceptance Scenarios**:

1. **Given** 用户注册时, **When** 密码存入数据库, **Then** 使用bcrypt加密（与Node.js版本兼容）
2. **Given** 用户登录成功, **When** 返回JWT token, **Then** token使用相同的密钥和算法（前端无需修改）
3. **Given** API接收用户输入, **When** 数据包含XSS攻击代码, **Then** 自动转义或拒绝请求
4. **Given** 使用SQLAlchemy ORM, **When** 执行数据库查询, **Then** 自动使用参数化查询防止SQL注入
5. **Given** API接口需要认证, **When** 请求未携带有效token, **Then** 返回401错误

---

### User Story 4 - 为LLM集成预留架构 (Priority: P2)

作为AI产品经理，我希望后端架构中预留清晰的LLM集成接口和服务层，以便后续快速接入大语言模型和RAG功能。

**Why this priority**: 这是迁移到Python的核心原因之一，需要提前规划。

**Independent Test**: 可以通过创建示例LLM服务和调用流程来验证架构可行性。

**Acceptance Scenarios**:

1. **Given** 后端架构设计, **When** 查看服务层, **Then** 包含独立的 `app/services/llm/` 目录用于AI服务
2. **Given** 创建LLM服务抽象, **When** 编写代码, **Then** 支持多个LLM提供商（OpenAI、Claude、本地模型）的适配器模式
3. **Given** 预留RAG功能, **When** 查看项目结构, **Then** 包含 `app/services/rag/` 和向量数据库配置
4. **Given** 技能数据存在, **When** 调用LLM服务, **Then** 可以将技能描述、验收标准等作为上下文传递
5. **Given** LLM返回建议, **When** 系统处理响应, **Then** 将建议与用户技能数据关联并存储

---

### User Story 5 - 开发体验优化 (Priority: P2)

作为开发者，我希望Python后端具备良好的开发体验，包括热重载、自动API文档、完善的日志系统等。

**Why this priority**: 良好的开发体验能提高开发效率。

**Independent Test**: 可以通过运行开发服务器、访问API文档、查看日志输出来验证。

**Acceptance Scenarios**:

1. **Given** 使用uvicorn运行服务, **When** 修改代码, **Then** 自动热重载（开发模式）
2. **Given** 访问 `/docs` 路径, **When** 打开浏览器, **Then** 显示自动生成的Swagger API文档
3. **Given** 访问 `/redoc` 路径, **When** 打开浏览器, **Then** 显示ReDoc格式的API文档
4. **Given** API发生错误, **When** 查看控制台, **Then** 显示详细的堆栈信息和日志
5. **Given** 使用结构化日志, **When** 记录日志, **Then** 包含时间戳、日志级别、请求ID等信息

---

### User Story 6 - 数据库迁移与兼容 (Priority: P1)

作为数据库管理员，我希望Python后端能够使用现有的MySQL数据库，无需修改表结构，确保数据平滑迁移。

**Why this priority**: 保证数据不丢失是迁移的硬性要求。

**Independent Test**: 可以通过连接现有数据库、执行CRUD操作来验证兼容性。

**Acceptance Scenarios**:

1. **Given** 现有MySQL数据库, **When** Python后端启动, **Then** 成功连接并使用现有表结构
2. **Given** 使用SQLAlchemy定义模型, **When** 模型定义完成, **Then** 与现有表结构完全匹配
3. **Given** 使用Alembic管理迁移, **When** 需要修改表结构, **Then** 生成并执行迁移脚本
4. **Given** JSON字段存储技能数据, **When** 读取和写入, **Then** 正确处理JSON序列化和反序列化
5. **Given** 数据库连接池, **When** 高并发请求, **Then** 自动管理连接复用和释放

---

### Edge Cases

- **Node.js与Python JWT兼容性**: 确保使用相同的JWT密钥和算法，使现有token仍然有效
- **密码哈希兼容性**: Python的bcrypt必须能验证Node.js bcrypt生成的哈希
- **时区处理**: 统一使用UTC时间，与Node.js版本保持一致
- **并发写入**: 使用数据库事务和版本号避免冲突
- **API响应格式**: 确保错误码、字段名、数据类型与原版本完全一致
- **CORS配置**: 保持与Node.js版本相同的跨域策略
- **文件上传**: 如后续需要，预留文件处理机制
- **WebSocket支持**: 为实时通知预留架构（可选）

---

## Requirements *(mandatory)*

### Functional Requirements

**核心API功能:**
- **FR-001**: 系统必须提供用户注册接口 `POST /api/auth/register`
- **FR-002**: 系统必须提供用户登录接口 `POST /api/auth/login`
- **FR-003**: 系统必须提供获取用户信息接口 `GET /api/auth/me`
- **FR-004**: 系统必须提供获取技能数据接口 `GET /api/skills`
- **FR-005**: 系统必须提供更新技能数据接口 `PUT /api/skills`
- **FR-006**: 系统必须提供获取活动热力图接口 `GET /api/activity/heatmap`
- **FR-007**: 系统必须提供记录活动接口 `POST /api/activity`

**技术架构要求:**
- **FR-008**: 必须使用FastAPI作为Web框架
- **FR-009**: 必须使用SQLAlchemy 2.0+作为ORM
- **FR-010**: 必须使用Pydantic v2进行数据验证
- **FR-011**: 必须使用Poetry进行依赖管理
- **FR-012**: 必须使用python-dotenv管理环境变量
- **FR-013**: 必须使用aiomysql或asyncmy作为异步MySQL驱动

**安全要求:**
- **FR-014**: 必须使用bcrypt加密密码（兼容Node.js版本）
- **FR-015**: 必须使用PyJWT生成和验证JWT token
- **FR-016**: 必须实现JWT中间件自动验证token
- **FR-017**: 必须对用户输入进行XSS过滤（使用bleach或类似库）
- **FR-018**: 必须使用ORM参数化查询防止SQL注入
- **FR-019**: 必须实现CORS中间件（使用fastapi-cors）

**开发体验:**
- **FR-020**: 必须自动生成OpenAPI文档（FastAPI内置）
- **FR-021**: 必须提供健康检查接口 `GET /health`
- **FR-022**: 必须使用结构化日志（使用loguru或structlog）
- **FR-023**: 必须支持热重载（uvicorn --reload）
- **FR-024**: 必须提供Docker容器化支持

**LLM预留架构:**
- **FR-025**: 必须创建 `app/services/llm/` 服务层目录
- **FR-026**: 必须定义LLM服务抽象接口（支持多提供商）
- **FR-027**: 必须创建 `app/services/rag/` 目录用于RAG功能
- **FR-028**: 必须在配置中预留LLM API密钥配置项
- **FR-029**: 必须设计技能数据与LLM上下文的转换接口

**数据库兼容性:**
- **FR-030**: 必须使用现有MySQL数据库和表结构
- **FR-031**: 必须定义SQLAlchemy模型映射现有表
- **FR-032**: 必须使用Alembic进行数据库版本管理
- **FR-033**: 必须正确处理JSON字段的序列化
- **FR-034**: 必须实现数据库连接池管理

### Key Entities

**SQLAlchemy模型定义:**

- **User (用户模型)**:
  ```python
  class User(Base):
      __tablename__ = "users"
      
      id: Mapped[int] = mapped_column(primary_key=True)
      username: Mapped[str] = mapped_column(String(50), unique=True)
      email: Mapped[str] = mapped_column(String(100), unique=True)
      password_hash: Mapped[str] = mapped_column(String(255))
      created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
      last_login_at: Mapped[Optional[datetime]]
      is_active: Mapped[bool] = mapped_column(default=True)
      
      # 关系
      skill_data: Mapped["UserSkillData"] = relationship(back_populates="user")
      activity_logs: Mapped[list["ActivityLog"]] = relationship(back_populates="user")
  ```

- **UserSkillData (技能数据模型)**:
  ```python
  class UserSkillData(Base):
      __tablename__ = "user_skill_data"
      
      id: Mapped[int] = mapped_column(primary_key=True)
      user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
      skill_data: Mapped[dict] = mapped_column(JSON)  # 完整的技能数据
      last_modified: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
      version: Mapped[int] = mapped_column(default=1)
      
      # 关系
      user: Mapped["User"] = relationship(back_populates="skill_data")
  ```

- **ActivityLog (活动日志模型)**:
  ```python
  class ActivityLog(Base):
      __tablename__ = "activity_logs"
      
      id: Mapped[int] = mapped_column(primary_key=True)
      user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
      activity_date: Mapped[date] = mapped_column(Date)
      activity_count: Mapped[int] = mapped_column(default=0)
      details: Mapped[Optional[dict]] = mapped_column(JSON)
      created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
      
      # 关系
      user: Mapped["User"] = relationship(back_populates="activity_logs")
      
      # 唯一约束
      __table_args__ = (
          UniqueConstraint('user_id', 'activity_date', name='unique_user_date'),
      )
  ```

**Pydantic Schema定义:**

- **UserRegister (注册请求)**:
  ```python
  class UserRegister(BaseModel):
      username: str = Field(min_length=3, max_length=50)
      email: EmailStr
      password: str = Field(min_length=8, pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)")
  ```

- **UserLogin (登录请求)**:
  ```python
  class UserLogin(BaseModel):
      username_or_email: str
      password: str
  ```

- **TokenResponse (Token响应)**:
  ```python
  class TokenResponse(BaseModel):
      token: str
      user: UserOut
  ```

- **SkillDataUpdate (技能数据更新)**:
  ```python
  class SkillDataUpdate(BaseModel):
      skill_data: dict  # 完整的技能JSON
      version: int  # 版本号用于冲突检测
  ```

**LLM服务抽象接口:**

- **LLMProvider (LLM提供商抽象)**:
  ```python
  class LLMProvider(ABC):
      @abstractmethod
      async def generate(self, prompt: str, context: dict) -> str:
          """生成LLM响应"""
          pass
      
      @abstractmethod
      async def embed(self, text: str) -> list[float]:
          """生成文本嵌入向量"""
          pass
  ```

- **SkillRecommendationService (技能推荐服务)**:
  ```python
  class SkillRecommendationService:
      def __init__(self, llm_provider: LLMProvider):
          self.llm = llm_provider
      
      async def get_next_skill_suggestions(self, user_id: int) -> list[str]:
          """基于用户当前进度推荐下一步技能"""
          pass
      
      async def generate_practice_tips(self, skill_id: str, level: int) -> str:
          """为特定技能等级生成练习建议"""
          pass
  ```

---

## Technical Architecture

### 项目结构

```
backend-python/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI应用入口
│   ├── api/                       # API路由层
│   │   ├── __init__.py
│   │   ├── deps.py               # 依赖注入（获取当前用户、数据库session等）
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py           # 认证相关接口
│   │       ├── skills.py         # 技能管理接口
│   │       └── activity.py       # 活动日志接口
│   ├── core/                      # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py             # 配置管理（从环境变量读取）
│   │   ├── security.py           # 安全工具（密码加密、JWT等）
│   │   └── database.py           # 数据库连接池
│   ├── models/                    # SQLAlchemy模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── skill_data.py
│   │   └── activity_log.py
│   ├── schemas/                   # Pydantic模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── skill.py
│   │   ├── activity.py
│   │   └── common.py             # 通用响应格式
│   ├── services/                  # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── skill_service.py
│   │   ├── activity_service.py
│   │   ├── llm/                  # LLM服务（预留）
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # LLM抽象接口
│   │   │   ├── openai_provider.py
│   │   │   └── claude_provider.py
│   │   └── rag/                  # RAG服务（预留）
│   │       ├── __init__.py
│   │       ├── vector_store.py   # 向量数据库接口
│   │       └── retriever.py      # 检索服务
│   ├── middleware/                # 中间件
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── cors_middleware.py
│   │   └── logging_middleware.py
│   └── utils/                     # 工具函数
│       ├── __init__.py
│       ├── xss_filter.py
│       └── response.py           # 统一响应格式
├── alembic/                       # 数据库迁移
│   ├── versions/
│   └── env.py
├── tests/                         # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_skills.py
│   └── test_activity.py
├── scripts/                       # 脚本
│   ├── init_db.py                # 数据库初始化
│   └── test_api.py               # API测试脚本
├── .env.example                   # 环境变量示例
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml                 # Poetry配置
├── poetry.lock
└── README.md
```

### 技术栈

**核心框架:**
- FastAPI 0.104+ (异步Web框架)
- SQLAlchemy 2.0+ (异步ORM)
- Pydantic v2 (数据验证)
- Uvicorn (ASGI服务器)

**数据库:**
- MySQL 8.0+
- aiomysql 或 asyncmy (异步MySQL驱动)
- Alembic (数据库迁移)

**安全:**
- python-jose[cryptography] (JWT处理)
- passlib[bcrypt] (密码加密)
- bleach (XSS过滤)

**开发工具:**
- Poetry (依赖管理)
- python-dotenv (环境变量)
- loguru (日志系统)
- pytest (测试框架)
- black (代码格式化)
- ruff (代码检查)

**LLM相关（预留）:**
- openai (OpenAI API)
- anthropic (Claude API)
- langchain (LLM框架)
- chromadb 或 qdrant (向量数据库)

### API响应格式统一

所有API响应必须遵循以下格式（与Node.js版本保持一致）:

**成功响应:**
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

**错误响应:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": { ... }
  }
}
```

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

**功能完整性:**
- **SC-001**: 100%的现有API接口成功迁移（注册、登录、技能管理、活动日志）
- **SC-002**: 前端应用无需修改代码即可正常工作
- **SC-003**: 通过所有现有的API测试用例（test-api.ps1）

**性能指标:**
- **SC-004**: API平均响应时间 < 200ms（与Node.js版本相当或更好）
- **SC-005**: 支持至少100并发用户（压力测试）
- **SC-006**: 数据库连接池复用率 > 90%

**安全性:**
- **SC-007**: 密码加密兼容性100%（能验证Node.js版本创建的用户）
- **SC-008**: JWT token兼容性100%（现有token仍然有效）
- **SC-009**: 通过OWASP Top 10基础安全检测

**代码质量:**
- **SC-010**: 代码测试覆盖率 > 80%
- **SC-011**: 所有API接口有完整的类型注解
- **SC-012**: 通过black和ruff代码检查

**开发体验:**
- **SC-013**: API文档自动生成并可通过 `/docs` 访问
- **SC-014**: 开发模式下支持热重载
- **SC-015**: 完整的Docker容器化支持

**架构扩展性:**
- **SC-016**: LLM服务接口定义清晰，支持至少2种提供商（OpenAI、Claude）
- **SC-017**: RAG功能架构预留完整，包含向量存储接口
- **SC-018**: 代码模块化程度高，新增LLM功能不影响现有API

**部署准备:**
- **SC-019**: 提供完整的部署文档和Docker配置
- **SC-020**: 数据库迁移脚本测试通过（从Node.js版本数据无缝迁移）

---

## Migration Strategy

### 迁移步骤

**Phase 1: 环境准备（1天）**
1. 创建 `backend-python` 目录
2. 初始化Poetry项目和依赖
3. 配置开发环境（.env、Docker）
4. 建立项目目录结构

**Phase 2: 核心架构（2-3天）**
1. 实现数据库连接和SQLAlchemy模型
2. 创建Pydantic schemas
3. 实现JWT认证和密码加密（确保兼容性）
4. 搭建FastAPI基础架构

**Phase 3: API迁移（3-4天）**
1. 迁移认证接口（注册、登录）
2. 迁移技能管理接口
3. 迁移活动日志接口
4. 统一响应格式和错误处理

**Phase 4: 测试与验证（2天）**
1. 编写单元测试
2. 运行API兼容性测试
3. 前后端集成测试
4. 性能测试和优化

**Phase 5: LLM架构预留（1-2天）**
1. 设计LLM服务抽象接口
2. 创建示例LLM集成（OpenAI）
3. 设计RAG架构
4. 文档编写

### 兼容性验证清单

- [ ] JWT token格式和加密算法一致
- [ ] bcrypt密码哈希兼容（salt rounds相同）
- [ ] API请求/响应格式完全一致
- [ ] 错误码和错误信息保持一致
- [ ] 时间戳格式统一（ISO 8601）
- [ ] CORS策略保持一致
- [ ] 数据库字段映射正确
- [ ] JSON序列化/反序列化正确

### 回滚计划

如迁移过程中出现问题，可以：
1. 保留Node.js版本作为备份
2. 使用相同的数据库（两个后端可以共存）
3. 通过Nginx或负载均衡器快速切换后端
4. 数据库无需回滚（表结构未变）

---

## Future Enhancements

### LLM功能规划（Phase 2）

1. **智能技能推荐**:
   - 基于用户当前进度，使用LLM推荐下一步应该学习的技能
   - 分析用户的学习路径，提供个性化建议

2. **练习内容生成**:
   - 为每个技能等级动态生成练习题和挑战
   - 根据用户薄弱环节生成针对性训练内容

3. **学习日志分析**:
   - 使用LLM分析用户的练习日志，提取关键学习点
   - 识别学习中的困难和突破

4. **智能导师对话**:
   - 提供基于RAG的技能问答功能
   - 结合技能知识库回答用户的学习问题

### RAG功能规划（Phase 3）

1. **技能知识库构建**:
   - 将所有技能描述、验收标准、Boss挑战向量化
   - 构建专业领域知识库（AI产品、销售等）

2. **上下文检索**:
   - 用户提问时自动检索相关技能内容
   - 基于用户当前等级提供精准的学习资源

3. **个性化内容推荐**:
   - 根据用户学习历史推荐相关文章、视频
   - 匹配用户能力水平的学习材料

---

## Notes

- 本次迁移保持API接口不变，确保前端零改动
- 重点是为后续AI功能预留清晰的架构
- 数据库表结构不变，只是访问方式从Node.js改为Python
- 优先保证功能完整性和兼容性，性能优化可在迁移后进行
- LLM和RAG功能在本次迁移中只做架构预留，不实现具体功能
