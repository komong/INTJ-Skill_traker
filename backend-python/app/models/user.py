"""
User模型
映射数据库的users表
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    """用户模型"""

    __tablename__ = "users"

    # 字段定义
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户唯一标识")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="用户名(唯一)")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="邮箱地址(唯一)")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment="bcrypt加密后的密码哈希")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True, comment="注册时间")
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="最后登录时间")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="账户是否激活(1=激活,0=禁用)")

    # 关系定义
    skill_data: Mapped[Optional["UserSkillData"]] = relationship("UserSkillData", back_populates="user", uselist=False, cascade="all, delete-orphan")
    activity_logs: Mapped[List["ActivityLog"]] = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
