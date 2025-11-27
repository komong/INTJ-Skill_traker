"""
ActivityLog模型
映射数据库的activity_logs表
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
from sqlalchemy import Integer, Date, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ActivityLog(Base):
    """用户活动日志模型"""

    __tablename__ = "activity_logs"

    # 字段定义
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="记录唯一标识")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="关联的用户ID")
    activity_date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="活动日期")
    activity_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="当天的活动次数")
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, comment="详细活动记录(JSON格式)")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="记录创建时间")

    # 关系定义
    user: Mapped["User"] = relationship("User", back_populates="activity_logs")

    # 表级约束
    __table_args__ = (
        UniqueConstraint('user_id', 'activity_date', name='unique_user_date'),
    )

    def __repr__(self) -> str:
        return f"<ActivityLog(id={self.id}, user_id={self.user_id}, date={self.activity_date}, count={self.activity_count})>"
