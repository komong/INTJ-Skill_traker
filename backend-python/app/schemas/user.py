"""
用户相关的Pydantic Schemas
定义用户注册、登录、响应等数据格式
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserRegister(BaseModel):
    """用户注册请求"""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="用户名，3-50个字符"
    )
    email: EmailStr = Field(
        ...,
        description="邮箱地址"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="密码，至少8位，包含大小写字母和数字"
    )
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """验证密码强度"""
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含小写字母')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含大写字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含数字')
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "john@example.com",
                    "password": "Test@1234"
                }
            ]
        }
    }


class UserLogin(BaseModel):
    """用户登录请求"""
    username_or_email: str = Field(
        ...,
        description="用户名或邮箱"
    )
    password: str = Field(
        ...,
        description="密码"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username_or_email": "johndoe",
                    "password": "Test@1234"
                }
            ]
        }
    }


class UserOut(BaseModel):
    """用户信息响应（不包含密码）"""
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    created_at: datetime = Field(..., description="注册时间", alias="createdAt")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间", alias="lastLoginAt")
    is_active: bool = Field(..., description="账户是否激活", alias="isActive")
    
    model_config = {
        "from_attributes": True,  # 允许从ORM模型创建
        "populate_by_name": True,  # 允许使用字段名或别名
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com",
                    "createdAt": "2025-11-26T10:00:00Z",
                    "lastLoginAt": "2025-11-26T12:00:00Z",
                    "isActive": True
                }
            ]
        }
    }


class TokenResponse(BaseModel):
    """JWT Token响应"""
    token: str = Field(..., description="JWT访问令牌")
    user: UserOut = Field(..., description="用户信息")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "user": {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@example.com",
                        "created_at": "2025-11-26T10:00:00Z",
                        "last_login_at": "2025-11-26T12:00:00Z",
                        "is_active": True
                    }
                }
            ]
        }
    }
