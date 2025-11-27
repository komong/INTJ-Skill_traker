"""
安全模块
包含密码加密、JWT处理等安全相关功能
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import bcrypt
from jose import JWTError, jwt
from loguru import logger

from app.core.config import settings

# ====================================
# 密码加密配置
# ====================================

# bcrypt salt rounds（与Node.js版本保持一致）
BCRYPT_SALT_ROUNDS = 12


def hash_password(password: str) -> str:
    """
    使用bcrypt加密密码
    
    Args:
        password: 明文密码
        
    Returns:
        str: 加密后的密码哈希
    """
    # 将密码转为bytes
    password_bytes = password.encode('utf-8')
    # 生成salt
    salt = bcrypt.gensalt(rounds=BCRYPT_SALT_ROUNDS)
    # 加密
    hashed = bcrypt.hashpw(password_bytes, salt)
    # 返回字符串
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    Args:
        plain_password: 明文密码
        hashed_password: 数据库中的密码哈希
        
    Returns:
        bool: 密码是否匹配
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"密码验证失败: {e}")
        return False


# ====================================
# JWT Token处理
# ====================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    
    Args:
        data: 要编码的数据（通常包含user_id等）
        expires_delta: 过期时间增量，默认使用配置的24小时
        
    Returns:
        str: JWT token字符串
    """
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # 使用与Node.js相同的算法和密钥
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码JWT访问令牌
    
    Args:
        token: JWT token字符串
        
    Returns:
        Optional[Dict[str, Any]]: 解码后的payload，失败返回None
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT解码失败: {e}")
        return None
    except Exception as e:
        logger.error(f"Token解码异常: {e}")
        return None


def verify_token(token: str) -> Optional[int]:
    """
    验证token并返回用户ID
    
    Args:
        token: JWT token字符串
        
    Returns:
        Optional[int]: 用户ID，失败返回None
    """
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    user_id: Optional[int] = payload.get("user_id")
    return user_id
