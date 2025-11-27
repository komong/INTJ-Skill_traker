"""
UserSkillData模型
映射数据库的user_skill_data表
"""

from datetime import datetime
from typing import Dict, Any
from sqlalchemy import Integer, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserSkillData(Base):
    """用户技能数据模型"""

    __tablename__ = "user_skill_data"

    # 字段定义
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="记录唯一标识")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="关联的用户ID")
    skill_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, comment="完整的技能数据(JSON格式)")
    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        index=True,
        comment="最后修改时间"
    )
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="数据版本号(用于冲突检测)")

    # 关系定义
    user: Mapped["User"] = relationship("User", back_populates="skill_data")

    def __repr__(self) -> str:
        return f"<UserSkillData(id={self.id}, user_id={self.user_id}, version={self.version})>"
