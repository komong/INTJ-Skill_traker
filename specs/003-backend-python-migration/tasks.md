# Tasks: 后端架构迁移至Python

**Feature**: `003-backend-python-migration`  
**Status**: Not Started

## Task Checklist

### Phase 1: 环境准备与项目初始化 ✅

- [ ] 创建 `backend-python` 目录
- [ ] 初始化Poetry项目 (`poetry init`)
- [ ] 添加核心依赖到 `pyproject.toml`:
  - [ ] FastAPI >= 0.104
  - [ ] SQLAlchemy >= 2.0
  - [ ] Pydantic >= 2.0
  - [ ] aiomysql 或 asyncmy
  - [ ] python-jose[cryptography]
  - [ ] passlib[bcrypt]
  - [ ] uvicorn[standard]
  - [ ] python-dotenv
- [ ] 添加开发依赖:
  - [ ] pytest
  - [ ] pytest-asyncio
  - [ ] black
  - [ ] ruff
  - [ ] mypy
- [ ] 创建项目目录结构:
  ```
  backend-python/
  ├── app/
  │   ├── api/v1/
  │   ├── core/
  │   ├── models/
  │   ├── schemas/
  │   ├── services/
  │   │   ├── llm/
  │   │   └── rag/
  │   ├── middleware/
  │   └── utils/
  ├── tests/
  ├── scripts/
  └── alembic/
  ```
- [ ] 创建 `.env.example` 配置模板
- [ ] 创建 `app/main.py` 基础文件
- [ ] 测试 `poetry install` 成功
- [ ] 测试 `uvicorn app.main:app --reload` 启动成功

---

### Phase 2: 数据库层实现 🔧

#### 2.1 数据库连接配置
- [ ] 创建 `app/core/config.py` 配置管理类
  - [ ] 使用Pydantic Settings加载环境变量
  - [ ] 定义数据库连接参数
  - [ ] 定义JWT配置（与Node.js保持一致）
- [ ] 创建 `app/core/database.py` 数据库连接
  - [ ] 创建异步数据库引擎
  - [ ] 配置连接池（connectionLimit: 10）
  - [ ] 实现 `async_session_factory`
  - [ ] 实现 `get_db()` 依赖注入函数

#### 2.2 SQLAlchemy模型定义
- [ ] 创建 `app/models/base.py` 基础模型类
- [ ] 创建 `app/models/user.py` User模型
  - [ ] 映射 `users` 表
  - [ ] 字段：id, username, email, password_hash, created_at, last_login_at, is_active
  - [ ] 索引：username, email, created_at
- [ ] 创建 `app/models/skill_data.py` UserSkillData模型
  - [ ] 映射 `user_skill_data` 表
  - [ ] 字段：id, user_id, skill_data (JSON), last_modified, version
  - [ ] 外键关系：user_id -> users.id
- [ ] 创建 `app/models/activity_log.py` ActivityLog模型
  - [ ] 映射 `activity_logs` 表
  - [ ] 字段：id, user_id, activity_date, activity_count, details (JSON), created_at
  - [ ] 唯一约束：(user_id, activity_date)
- [ ] 在 `app/models/__init__.py` 中导出所有模型

#### 2.3 Alembic配置
- [ ] 初始化Alembic (`alembic init alembic`)
- [ ] 配置 `alembic/env.py` 连接数据库
- [ ] 导入所有模型到 `env.py`
- [ ] 生成初始迁移 (`alembic revision --autogenerate -m "initial"`)
- [ ] 验证迁移脚本不会修改现有表

#### 2.4 数据库测试
- [ ] 创建 `scripts/test_db.py` 测试脚本
- [ ] 测试数据库连接成功
- [ ] 测试读取现有测试用户
- [ ] 测试JSON字段序列化/反序列化
- [ ] 测试所有模型的CRUD操作

---

### Phase 3: 安全模块实现 🔒

#### 3.1 密码加密
- [ ] 创建 `app/core/security.py`
- [ ] 实现 `hash_password(password: str) -> str`
  - [ ] 使用passlib的bcrypt
  - [ ] 配置salt rounds = 12（与Node.js一致）
- [ ] 实现 `verify_password(plain: str, hashed: str) -> bool`
- [ ] 测试与Node.js bcrypt的兼容性
  - [ ] 验证Node.js创建的哈希
  - [ ] Python创建的哈希被Node.js验证

#### 3.2 JWT处理
- [ ] 实现 `create_access_token(data: dict, expires_delta: timedelta = None) -> str`
  - [ ] 使用python-jose
  - [ ] 算法：HS256（与Node.js一致）
  - [ ] 过期时间：24小时
- [ ] 实现 `decode_access_token(token: str) -> dict`
  - [ ] 验证签名
  - [ ] 检查过期时间
  - [ ] 处理异常（过期、无效等）
- [ ] 测试JWT兼容性
  - [ ] 验证Node.js生成的token
  - [ ] Python生成的token被Node.js验证

#### 3.3 认证依赖
- [ ] 创建 `app/api/deps.py`
- [ ] 定义 `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")`
- [ ] 实现 `async def get_current_user(token: str, db: AsyncSession) -> User`
  - [ ] 从header提取token
  - [ ] 解码并验证token
  - [ ] 从数据库加载用户
  - [ ] 处理未授权错误（401）

#### 3.4 XSS过滤
- [ ] 创建 `app/utils/xss_filter.py`
- [ ] 安装bleach库
- [ ] 实现 `sanitize_html(text: str) -> str`
- [ ] 测试XSS攻击代码过滤

---

### Phase 4: Pydantic Schemas定义 📋

#### 4.1 用户schemas
- [ ] 创建 `app/schemas/user.py`
- [ ] 定义 `UserRegister`
  - [ ] username: str (3-50字符)
  - [ ] email: EmailStr
  - [ ] password: str (至少8位，包含大小写字母和数字)
- [ ] 定义 `UserLogin`
  - [ ] username_or_email: str
  - [ ] password: str
- [ ] 定义 `UserOut`
  - [ ] id, username, email, created_at
  - [ ] 排除password_hash
- [ ] 定义 `TokenResponse`
  - [ ] token: str
  - [ ] user: UserOut

#### 4.2 技能schemas
- [ ] 创建 `app/schemas/skill.py`
- [ ] 定义 `SkillDataOut`
  - [ ] skill_data: dict
  - [ ] last_modified: datetime
  - [ ] version: int
- [ ] 定义 `SkillDataUpdate`
  - [ ] skill_data: dict
  - [ ] version: int

#### 4.3 活动schemas
- [ ] 创建 `app/schemas/activity.py`
- [ ] 定义 `ActivityCreate`
  - [ ] details: dict
- [ ] 定义 `ActivityOut`
  - [ ] id, user_id, activity_date, activity_count, details
- [ ] 定义 `HeatmapData`
  - [ ] date: str
  - [ ] count: int
  - [ ] level: int
- [ ] 定义 `HeatmapResponse`
  - [ ] data: list[HeatmapData]

#### 4.4 通用响应
- [ ] 创建 `app/schemas/common.py`
- [ ] 定义 `SuccessResponse[T]` 泛型
  - [ ] success: bool = True
  - [ ] data: T
  - [ ] message: str
- [ ] 定义 `ErrorResponse`
  - [ ] success: bool = False
  - [ ] error: ErrorDetail
- [ ] 定义 `ErrorDetail`
  - [ ] code: str
  - [ ] message: str
  - [ ] details: dict | None

---

### Phase 5: 认证API实现 🔐

#### 5.1 认证服务
- [ ] 创建 `app/services/auth_service.py`
- [ ] 实现 `async def register_user(user_data: UserRegister, db: AsyncSession) -> User`
  - [ ] 检查用户名和邮箱是否已存在
  - [ ] 哈希密码
  - [ ] 创建用户记录
  - [ ] 创建初始技能数据记录（空数组）
  - [ ] 返回用户对象
- [ ] 实现 `async def authenticate_user(username_or_email: str, password: str, db: AsyncSession) -> User | None`
  - [ ] 查询用户（支持用户名或邮箱）
  - [ ] 验证密码
  - [ ] 更新last_login_at
  - [ ] 返回用户或None
- [ ] 实现 `async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None`

#### 5.2 认证路由
- [ ] 创建 `app/api/v1/auth.py`
- [ ] 实现 `POST /api/auth/register`
  - [ ] 接收UserRegister
  - [ ] 调用register_user服务
  - [ ] 生成JWT token
  - [ ] 返回TokenResponse（与Node.js格式一致）
  - [ ] 错误处理：用户名已存在、邮箱已存在
- [ ] 实现 `POST /api/auth/login`
  - [ ] 接收UserLogin
  - [ ] 调用authenticate_user服务
  - [ ] 生成JWT token
  - [ ] 返回TokenResponse
  - [ ] 错误处理：用户不存在、密码错误
- [ ] 实现 `GET /api/auth/me`
  - [ ] 需要认证（使用get_current_user依赖）
  - [ ] 返回UserOut

#### 5.3 响应格式工具
- [ ] 创建 `app/utils/response.py`
- [ ] 实现 `success_response(data: Any, message: str = "Success") -> dict`
- [ ] 实现 `error_response(code: str, message: str, details: dict = None) -> dict`

#### 5.4 单元测试
- [ ] 创建 `tests/test_auth.py`
- [ ] 测试注册成功
- [ ] 测试注册失败（用户名已存在）
- [ ] 测试注册失败（密码强度不足）
- [ ] 测试登录成功
- [ ] 测试登录失败（用户不存在）
- [ ] 测试登录失败（密码错误）
- [ ] 测试获取当前用户信息
- [ ] 测试未授权访问

---

### Phase 6: 技能管理API实现 📊

#### 6.1 技能服务
- [ ] 创建 `app/services/skill_service.py`
- [ ] 实现 `async def get_user_skills(user_id: int, db: AsyncSession) -> dict`
  - [ ] 查询UserSkillData记录
  - [ ] 如果不存在，返回默认空数据
  - [ ] 返回skill_data和version
- [ ] 实现 `async def update_user_skills(user_id: int, skill_data: dict, version: int, db: AsyncSession) -> UserSkillData`
  - [ ] 查询当前记录
  - [ ] 检查版本号（乐观锁）
  - [ ] 如果版本不匹配，抛出冲突异常
  - [ ] 更新skill_data和version（+1）
  - [ ] 提交事务
  - [ ] 返回更新后的记录

#### 6.2 技能路由
- [ ] 创建 `app/api/v1/skills.py`
- [ ] 实现 `GET /api/skills`
  - [ ] 需要认证
  - [ ] 调用get_user_skills服务
  - [ ] 返回SkillDataOut（包装在success_response中）
- [ ] 实现 `PUT /api/skills`
  - [ ] 需要认证
  - [ ] 接收SkillDataUpdate
  - [ ] 调用update_user_skills服务
  - [ ] 返回更新后的数据
  - [ ] 错误处理：版本冲突（409 Conflict）

#### 6.3 单元测试
- [ ] 创建 `tests/test_skills.py`
- [ ] 测试获取技能数据（有数据）
- [ ] 测试获取技能数据（无数据返回默认）
- [ ] 测试更新技能数据成功
- [ ] 测试版本冲突检测
- [ ] 测试未授权访问
- [ ] 测试跨用户访问（应失败）

---

### Phase 7: 活动日志API实现 📈

#### 7.1 活动服务
- [ ] 创建 `app/services/activity_service.py`
- [ ] 实现 `async def record_activity(user_id: int, details: dict, db: AsyncSession) -> ActivityLog`
  - [ ] 获取今天的日期
  - [ ] 查询今天的ActivityLog记录
  - [ ] 如果存在，更新activity_count和details
  - [ ] 如果不存在，创建新记录
  - [ ] 使用ON DUPLICATE KEY UPDATE或merge
  - [ ] 返回记录
- [ ] 实现 `async def get_heatmap_data(user_id: int, days: int, db: AsyncSession) -> list[dict]`
  - [ ] 计算起始日期（today - days）
  - [ ] 查询activity_date >= start_date的记录
  - [ ] 按日期排序
  - [ ] 计算level（0-4，基于activity_count分段）
  - [ ] 返回 `[{"date": "YYYY-MM-DD", "count": N, "level": L}]`

#### 7.2 活动路由
- [ ] 创建 `app/api/v1/activity.py`
- [ ] 实现 `POST /api/activity`
  - [ ] 需要认证
  - [ ] 接收ActivityCreate
  - [ ] 调用record_activity服务
  - [ ] 返回ActivityOut
- [ ] 实现 `GET /api/activity/heatmap?days=365`
  - [ ] 需要认证
  - [ ] 查询参数：days (默认365)
  - [ ] 调用get_heatmap_data服务
  - [ ] 返回HeatmapResponse

#### 7.3 热力图level计算
- [ ] 定义level规则:
  - [ ] level 0: count = 0
  - [ ] level 1: count = 1-2
  - [ ] level 2: count = 3-5
  - [ ] level 3: count = 6-10
  - [ ] level 4: count > 10

#### 7.4 单元测试
- [ ] 创建 `tests/test_activity.py`
- [ ] 测试记录活动（首次）
- [ ] 测试记录活动（更新今天的记录）
- [ ] 测试获取热力图数据
- [ ] 测试热力图日期范围过滤
- [ ] 测试热力图level计算正确性

---

### Phase 8: 中间件和错误处理 🛡️

#### 8.1 CORS中间件
- [ ] 在 `app/main.py` 配置CORS
  - [ ] 使用 `fastapi.middleware.cors.CORSMiddleware`
  - [ ] allow_origins: ["*"] (开发模式)
  - [ ] allow_methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
  - [ ] allow_headers: ["Content-Type", "Authorization"]
  - [ ] allow_credentials: True

#### 8.2 日志中间件
- [ ] 创建 `app/middleware/logging_middleware.py`
- [ ] 安装loguru库
- [ ] 实现请求日志中间件
  - [ ] 记录请求方法、路径
  - [ ] 记录响应状态码
  - [ ] 记录处理时间
  - [ ] 使用结构化日志格式

#### 8.3 全局异常处理
- [ ] 在 `app/main.py` 添加异常处理器
- [ ] 处理 `HTTPException`
  - [ ] 返回统一的error_response格式
- [ ] 处理 `RequestValidationError` (Pydantic验证错误)
  - [ ] 提取详细的验证错误信息
  - [ ] 返回友好的错误提示
- [ ] 处理通用Exception
  - [ ] 记录详细的错误日志和堆栈
  - [ ] 返回通用的500错误（隐藏内部细节）

#### 8.4 健康检查
- [ ] 在 `app/main.py` 实现 `GET /health`
  - [ ] 检查服务状态
  - [ ] 检查数据库连接
  - [ ] 返回 `{ "success": true, "message": "...", "timestamp": "..." }`

#### 8.5 测试
- [ ] 测试CORS跨域请求
- [ ] 测试请求日志输出
- [ ] 测试验证错误响应格式
- [ ] 测试未处理异常的错误响应
- [ ] 测试/health接口

---

### Phase 9: LLM架构预留 🤖

#### 9.1 LLM服务抽象
- [ ] 创建 `app/services/llm/base.py`
- [ ] 定义 `LLMProvider` 抽象基类
  ```python
  class LLMProvider(ABC):
      @abstractmethod
      async def generate(self, prompt: str, context: dict) -> str:
          pass
      
      @abstractmethod
      async def embed(self, text: str) -> list[float]:
          pass
  ```

#### 9.2 OpenAI提供商
- [ ] 创建 `app/services/llm/openai_provider.py`
- [ ] 实现 `OpenAIProvider(LLMProvider)`
- [ ] 实现 `generate()` 方法（调用OpenAI API）
- [ ] 实现 `embed()` 方法（调用embeddings API）
- [ ] 配置API密钥和模型参数
- [ ] 添加示例调用（注释掉，仅作示例）

#### 9.3 Claude提供商
- [ ] 创建 `app/services/llm/claude_provider.py`
- [ ] 实现 `ClaudeProvider(LLMProvider)`
- [ ] 实现 `generate()` 方法（调用Anthropic API）
- [ ] 添加示例调用（注释掉，仅作示例）

#### 9.4 技能推荐服务
- [ ] 创建 `app/services/llm/skill_recommendation.py`
- [ ] 定义 `SkillRecommendationService`
- [ ] 定义接口方法（暂不实现）:
  - [ ] `async def get_next_skill_suggestions(user_id: int) -> list[str]`
  - [ ] `async def generate_practice_tips(skill_id: str, level: int) -> str`
  - [ ] `async def analyze_learning_logs(user_id: int) -> dict`

#### 9.5 RAG架构
- [ ] 创建 `app/services/rag/vector_store.py`
- [ ] 定义 `VectorStore` 抽象接口
  ```python
  class VectorStore(ABC):
      @abstractmethod
      async def add_texts(self, texts: list[str], metadata: list[dict]) -> None:
          pass
      
      @abstractmethod
      async def similarity_search(self, query: str, k: int = 5) -> list[dict]:
          pass
  ```
- [ ] 创建 `app/services/rag/retriever.py`
- [ ] 定义 `RAGRetriever` 接口（暂不实现）

#### 9.6 配置更新
- [ ] 在 `app/core/config.py` 添加LLM配置
  - [ ] OPENAI_API_KEY
  - [ ] ANTHROPIC_API_KEY
  - [ ] LLM_MODEL_NAME
  - [ ] LLM_TEMPERATURE
  - [ ] VECTOR_DB_URL

#### 9.7 文档
- [ ] 在README中添加LLM架构说明
- [ ] 说明如何扩展新的LLM提供商
- [ ] 说明如何集成RAG功能

---

### Phase 10: 测试与验证 ✅

#### 10.1 API兼容性测试
- [ ] 复制Node.js的 `test-api.ps1` 为 `test-api-python.ps1`
- [ ] 修改端口为Python后端端口（如8000）
- [ ] 运行所有API测试
- [ ] 验证响应格式与Node.js版本完全一致
- [ ] 记录并修复所有不一致的地方

#### 10.2 跨版本兼容性测试
- [ ] 使用Node.js后端注册用户
- [ ] 使用Python后端登录该用户
- [ ] 使用Node.js生成JWT token
- [ ] 使用Python后端验证该token
- [ ] 反向测试（Python创建，Node.js验证）

#### 10.3 集成测试
- [ ] 创建 `tests/test_integration.py`
- [ ] 端到端测试流程:
  - [ ] 注册用户
  - [ ] 登录获取token
  - [ ] 获取技能数据
  - [ ] 更新技能数据
  - [ ] 记录活动
  - [ ] 获取热力图
- [ ] 测试并发请求（多个用户同时操作）

#### 10.4 性能测试
- [ ] 安装locust或apache bench
- [ ] 创建 `tests/locustfile.py` 压力测试脚本
- [ ] 测试场景:
  - [ ] 100并发用户登录
  - [ ] 100并发用户更新技能数据
  - [ ] 1000次/秒获取热力图
- [ ] 记录性能指标:
  - [ ] 平均响应时间
  - [ ] P95响应时间
  - [ ] 最大并发数
  - [ ] 吞吐量（RPS）
- [ ] 验证响应时间 < 200ms（P95）

#### 10.5 安全测试
- [ ] XSS注入测试（在日志中注入脚本）
- [ ] SQL注入测试（尝试绕过ORM）
- [ ] JWT token篡改测试
- [ ] JWT token过期测试
- [ ] 未授权访问测试（无token访问受保护API）
- [ ] 跨用户访问测试（用户A访问用户B的数据）

#### 10.6 代码质量检查
- [ ] 运行 `black .` 格式化所有代码
- [ ] 运行 `ruff check .` 检查代码规范
- [ ] 修复所有ruff警告
- [ ] 运行 `mypy app/` 类型检查
- [ ] 修复所有类型错误
- [ ] 运行 `pytest --cov=app tests/` 查看测试覆盖率
- [ ] 确保覆盖率 > 80%

---

### Phase 11: Docker化与部署准备 🐳

#### 11.1 Dockerfile
- [ ] 创建 `Dockerfile`
- [ ] 使用多阶段构建:
  - [ ] Stage 1: 构建依赖（poetry install）
  - [ ] Stage 2: 运行环境（复制依赖和代码）
- [ ] 基础镜像：`python:3.11-slim`
- [ ] 安装系统依赖（如mysql客户端库）
- [ ] 复制项目文件
- [ ] 暴露8000端口
- [ ] 启动命令：`uvicorn app.main:app --host 0.0.0.0 --port 8000`

#### 11.2 docker-compose.yml
- [ ] 创建 `docker-compose.yml`
- [ ] 定义服务:
  - [ ] `backend-python`: Python后端服务
  - [ ] `mysql`: MySQL数据库服务（可选，如果不使用外部数据库）
- [ ] 配置网络
- [ ] 配置卷（数据持久化）
- [ ] 配置环境变量

#### 11.3 环境变量配置
- [ ] 更新 `.env.example` 包含所有配置项:
  ```
  # 数据库配置
  DB_HOST=localhost
  DB_PORT=3306
  DB_USER=root
  DB_PASSWORD=password
  DB_NAME=skill_tracker
  
  # JWT配置
  JWT_SECRET_KEY=your-secret-key
  JWT_ALGORITHM=HS256
  JWT_EXPIRE_HOURS=24
  
  # 服务配置
  PORT=8000
  DEBUG=False
  
  # LLM配置（可选）
  OPENAI_API_KEY=
  ANTHROPIC_API_KEY=
  ```
- [ ] 在README中说明所有环境变量

#### 11.4 部署脚本
- [ ] 创建 `scripts/deploy.sh` (Linux/Mac)
- [ ] 创建 `scripts/deploy.ps1` (Windows)
- [ ] 包含步骤:
  - [ ] 构建Docker镜像
  - [ ] 运行数据库迁移
  - [ ] 启动服务
  - [ ] 健康检查

#### 11.5 数据迁移文档
- [ ] 创建 `MIGRATION.md` 文档
- [ ] 说明从Node.js迁移的详细步骤:
  1. 备份数据库
  2. 停止Node.js服务
  3. 配置Python环境变量
  4. 运行Python服务
  5. 验证API功能
  6. 切换前端配置
  7. 监控日志
- [ ] 提供回滚步骤

#### 11.6 README更新
- [ ] 更新 `backend-python/README.md`
- [ ] 包含章节:
  - [ ] 项目简介
  - [ ] 技术栈
  - [ ] 本地开发环境搭建
    - [ ] 安装Poetry
    - [ ] 安装依赖
    - [ ] 配置环境变量
    - [ ] 运行开发服务器
  - [ ] Docker部署
  - [ ] API文档（链接到/docs）
  - [ ] 项目结构说明
  - [ ] LLM扩展指南
  - [ ] 测试运行方法

#### 11.7 测试部署
- [ ] 测试 `docker build` 成功
- [ ] 测试 `docker-compose up` 启动所有服务
- [ ] 测试容器内API正常工作
- [ ] 测试容器内访问数据库
- [ ] 测试环境变量正确加载

---

## Post-Implementation Checklist

### 功能验证
- [ ] 所有现有API接口100%迁移
- [ ] 前端应用无需修改即可工作
- [ ] 所有测试用例通过
- [ ] Node.js版本的测试脚本在Python后端上通过

### 性能验证
- [ ] API平均响应时间 < 200ms
- [ ] 支持100并发用户
- [ ] 数据库连接池正常工作
- [ ] 无明显内存泄漏

### 安全验证
- [ ] JWT token兼容性100%
- [ ] bcrypt密码兼容性100%
- [ ] XSS攻击防护有效
- [ ] SQL注入防护有效
- [ ] 未授权访问被正确拒绝

### 代码质量
- [ ] 测试覆盖率 > 80%
- [ ] 无black格式化警告
- [ ] 无ruff代码规范警告
- [ ] 无mypy类型错误
- [ ] 所有API有完整的类型注解

### 文档完整性
- [ ] README详细完整
- [ ] API文档自动生成（/docs可访问）
- [ ] 迁移文档清晰
- [ ] LLM扩展指南明确
- [ ] 环境变量说明完整

### 部署就绪
- [ ] Dockerfile构建成功
- [ ] docker-compose启动成功
- [ ] 部署脚本测试通过
- [ ] 提供回滚方案

---

## Notes

- 严格按照Phase顺序执行，确保每个阶段完成后再进入下一阶段
- 优先保证功能完整性和兼容性，性能优化可在迁移后进行
- LLM功能在本次只做架构预留，不实现具体调用
- 保留Node.js版本作为备份和对比参考
- 所有数据库操作使用异步方式（SQLAlchemy 2.0 async）
- 遵循FastAPI最佳实践和Python类型注解规范
