"""
技能数据服务层
处理技能数据的读取、更新和版本冲突检测
"""

from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.skill_data import UserSkillData


async def get_skill_data(db: AsyncSession, user_id: int) -> Optional[UserSkillData]:
    """
    获取用户的技能数据
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        Optional[UserSkillData]: 技能数据对象或None
    """
    result = await db.execute(
        select(UserSkillData).where(UserSkillData.user_id == user_id)
    )
    skill_data = result.scalar_one_or_none()
    
    if skill_data:
        logger.info(f"获取技能数据成功: user_id={user_id}, version={skill_data.version}")
    else:
        logger.warning(f"未找到技能数据: user_id={user_id}")
    
    return skill_data


async def update_skill_data(
    db: AsyncSession,
    user_id: int,
    new_skills: list,  # 改为技能数组
    client_version: int
) -> UserSkillData:
    """
    更新用户的技能数据（带版本冲突检测）
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        new_skills: 新的技能数组
        client_version: 客户端当前版本号
        
    Returns:
        UserSkillData: 更新后的技能数据对象
        
    Raises:
        ValueError: 版本冲突或数据不存在
    """
    # 查询当前数据
    result = await db.execute(
        select(UserSkillData).where(UserSkillData.user_id == user_id)
    )
    skill_data = result.scalar_one_or_none()
    
    if not skill_data:
        raise ValueError(f"技能数据不存在: user_id={user_id}")
    
    # 版本冲突检测（乐观锁）
    if skill_data.version != client_version:
        logger.warning(
            f"版本冲突: user_id={user_id}, "
            f"client_version={client_version}, "
            f"server_version={skill_data.version}"
        )
        raise ValueError(
            f"数据版本冲突，请刷新后重试。"
            f"客户端版本: {client_version}, 服务器版本: {skill_data.version}"
        )
    
    # 更新数据（直接存储数组）
    skill_data.skill_data = new_skills
    skill_data.last_modified = datetime.utcnow()
    skill_data.version = skill_data.version + 1
    
    await db.commit()
    await db.refresh(skill_data)
    
    logger.info(
        f"技能数据更新成功: user_id={user_id}, "
        f"new_version={skill_data.version}"
    )
    
    return skill_data
