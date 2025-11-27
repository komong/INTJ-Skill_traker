"""
数据库连接测试脚本
测试与MySQL数据库的连接和模型定义
"""

import sys
from pathlib import Path

# 将项目根目录添加到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from sqlalchemy import select
from loguru import logger

from app.core.database import init_db, close_db, async_session_factory
from app.models import User, UserSkillData, ActivityLog


async def test_db_connection():
    """测试数据库连接"""
    logger.info("=" * 50)
    logger.info("开始测试数据库连接...")
    logger.info("=" * 50)
    
    try:
        # 初始化数据库
        await init_db()
        
        # 测试查询现有用户
        async with async_session_factory() as session:
            # 查询用户数量
            result = await session.execute(select(User))
            users = result.scalars().all()
            logger.info(f"✅ 成功连接数据库")
            logger.info(f"📊 当前用户数量: {len(users)}")
            
            # 显示用户信息
            for user in users:
                logger.info(f"   - {user}")
                
            # 测试JSON字段查询
            if users:
                test_user = users[0]
                skill_result = await session.execute(
                    select(UserSkillData).where(UserSkillData.user_id == test_user.id)
                )
                skill_data = skill_result.scalar_one_or_none()
                if skill_data:
                    logger.info(f"✅ JSON字段读取成功: version={skill_data.version}")
                else:
                    logger.info("ℹ️  该用户暂无技能数据")
                    
            # 测试活动日志查询
            activity_result = await session.execute(select(ActivityLog))
            activities = activity_result.scalars().all()
            logger.info(f"📈 活动日志记录数: {len(activities)}")
            
        logger.info("=" * 50)
        logger.info("✅ 数据库测试完成!")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ 数据库测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(test_db_connection())
