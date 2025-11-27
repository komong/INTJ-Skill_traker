"""Pydantic Schemas"""

# 用户相关
from app.schemas.user import UserRegister, UserLogin, UserOut, TokenResponse

# 技能相关
from app.schemas.skill import SkillDataOut, SkillDataUpdate, SkillDataResponse

# 活动相关
from app.schemas.activity import (
    ActivityCreate,
    ActivityOut,
    HeatmapData,
    HeatmapResponse,
    ActivitySummary,
)

# 通用响应
from app.schemas.common import (
    ErrorDetail,
    ErrorResponse,
    SuccessResponse,
    MessageResponse,
    PaginationMeta,
    PaginatedResponse,
)

__all__ = [
    # 用户
    "UserRegister",
    "UserLogin",
    "UserOut",
    "TokenResponse",
    # 技能
    "SkillDataOut",
    "SkillDataUpdate",
    "SkillDataResponse",
    # 活动
    "ActivityCreate",
    "ActivityOut",
    "HeatmapData",
    "HeatmapResponse",
    "ActivitySummary",
    # 通用
    "ErrorDetail",
    "ErrorResponse",
    "SuccessResponse",
    "MessageResponse",
    "PaginationMeta",
    "PaginatedResponse",
]