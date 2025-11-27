from fastapi import FastAPI
from loguru import logger

from app.core.config import settings
from app.middleware import setup_cors, RequestLoggingMiddleware, setup_exception_handlers

# 创建FastAPI应用实例
app = FastAPI(
    title="Skill Tracker API",
    description="多维度技能追踪与成长可视化系统 - Python Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ====================================
# 注册中间件
# ====================================

# CORS中间件
setup_cors(app)

# 请求日志中间件
app.add_middleware(RequestLoggingMiddleware)

# 全局异常处理
setup_exception_handlers(app)

# ====================================
# 健康检查接口
# ====================================
@app.get("/health")
async def health_check():
    """健康检查接口"""
    from datetime import datetime
    
    return {
        "success": True,
        "message": "Skill Tracker API is running (Python/FastAPI)",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
    }


# ====================================
# 启动和关闭事件
# ====================================
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    from app.core.database import init_db
    
    # 初始化数据库连接
    await init_db()
    
    logger.info("🚀 Skill Tracker API Server Started")
    logger.info(f"📡 Port: {settings.PORT}")
    logger.info(f"🌍 Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"📝 API Docs: http://localhost:{settings.PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    from app.core.database import close_db
    
    await close_db()
    logger.info("📛 Skill Tracker API Server Shutting Down")


# ====================================
# 路由注册
# ====================================

from app.api.v1 import auth, skills, activity

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(activity.router, prefix="/api/activity", tags=["Activity"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
