"""
认证服务层
处理用户注册、登录等业务逻辑
"""

from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from loguru import logger

from app.models.user import User
from app.models.skill_data import UserSkillData
from app.core.security import hash_password, verify_password
from app.schemas.user import UserRegister


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    根据用户名查询用户
    
    Args:
        db: 数据库会话
        username: 用户名
        
    Returns:
        Optional[User]: 用户对象或None
    """
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    根据邮箱查询用户
    
    Args:
        db: 数据库会话
        email: 邮箱地址
        
    Returns:
        Optional[User]: 用户对象或None
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    根据ID查询用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        Optional[User]: 用户对象或None
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
    """
    注册新用户
    
    Args:
        db: 数据库会话
        user_data: 用户注册数据
        
    Returns:
        User: 新创建的用户对象
        
    Raises:
        ValueError: 用户名或邮箱已存在
    """
    # 检查用户名是否已存在
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise ValueError("用户名已存在")
    
    # 检查邮箱是否已存在
    existing_email = await get_user_by_email(db, user_data.email)
    if existing_email:
        raise ValueError("邮箱已被注册")
    
    # 加密密码
    password_hash = hash_password(user_data.password)
    
    # 创建用户
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        created_at=datetime.utcnow(),
        is_active=True
    )
    
    db.add(new_user)
    await db.flush()  # 刷新以获取user.id
    
    # 创建初始技能数据记录
    initial_skill_data = UserSkillData(
        user_id=new_user.id,
        skill_data=[],  # 空数组
        version=1
    )
    
    db.add(initial_skill_data)
    await db.commit()
    await db.refresh(new_user)
    
    logger.info(f"新用户注册成功: {new_user.username}")
    
    return new_user


async def authenticate_user(
    db: AsyncSession,
    username_or_email: str,
    password: str
) -> Optional[User]:
    """
    验证用户登录
    
    Args:
        db: 数据库会话
        username_or_email: 用户名或邮箱
        password: 密码
        
    Returns:
        Optional[User]: 验证成功返回用户对象，失败返回None
    """
    # 查询用户（支持用户名或邮箱）
    result = await db.execute(
        select(User).where(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        logger.warning(f"登录失败: 用户不存在 - {username_or_email}")
        return None
    
    # 验证密码
    if not verify_password(password, user.password_hash):
        logger.warning(f"登录失败: 密码错误 - {username_or_email}")
        return None
    
    # 检查账户是否激活
    if not user.is_active:
        logger.warning(f"登录失败: 账户未激活 - {username_or_email}")
        return None
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"用户登录成功: {user.username}")
    
    return user
