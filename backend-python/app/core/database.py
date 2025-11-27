"""
数据库连接模块
使用SQLAlchemy 2.0异步引擎
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from loguru import logger

from app.core.config import settings

# 创建异步数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 开发模式下显示SQL语句
    pool_size=10,  # 连接池大小(与Node.js版本对齐)
    max_overflow=0,
    pool_pre_ping=True,  # 连接前测试连接有效性
    pool_recycle=3600,  # 1小时后回收连接
)

# 创建异步会话工厂
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 创建声明式基类
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    数据库依赖注入函数
    用于FastAPI路由中获取数据库会话
    
    Yields:
        AsyncSession: 数据库会话对象
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    初始化数据库
    测试数据库连接
    """
    try:
        async with engine.begin() as conn:
            # 这里不创建表,因为我们使用现有的MySQL数据库
            # await conn.run_sync(Base.metadata.create_all)
            pass
        logger.info("✅ MySQL数据库连接成功")
    except Exception as e:
        logger.error(f"❌ MySQL数据库连接失败: {e}")
        raise


async def close_db() -> None:
    """关闭数据库连接"""
    await engine.dispose()
    logger.info("📛 数据库连接已关闭")
