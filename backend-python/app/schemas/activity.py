"""
活动日志相关的Pydantic Schemas
定义活动记录和热力图数据格式
"""

from datetime import datetime, date
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    """创建活动记录请求"""
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="活动详情（JSON格式）"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "details": {
                        "action": "complete_criteria",
                        "skill_id": "ai-agent-usage",
                        "level": 1,
                        "criteria_id": "1"
                    }
                }
            ]
        }
    }


class ActivityOut(BaseModel):
    """活动记录响应"""
    id: int = Field(..., description="记录ID")
    user_id: int = Field(..., description="用户ID")
    activity_date: date = Field(..., description="活动日期")
    activity_count: int = Field(..., description="当天活动次数")
    details: Optional[Dict[str, Any]] = Field(None, description="活动详情")
    created_at: datetime = Field(..., description="创建时间")
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "activity_date": "2025-11-26",
                    "activity_count": 5,
                    "details": {
                        "actions": [
                            {"type": "complete_criteria", "time": "10:30"}
                        ]
                    },
                    "created_at": "2025-11-26T10:00:00Z"
                }
            ]
        }
    }


class HeatmapData(BaseModel):
    """热力图单个数据点"""
    date: str = Field(..., description="日期（YYYY-MM-DD格式）")
    count: int = Field(..., description="活动次数")
    level: int = Field(..., description="热度等级（0-4）")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date": "2025-11-26",
                    "count": 5,
                    "level": 2
                }
            ]
        }
    }


class HeatmapResponse(BaseModel):
    """热力图数据响应"""
    data: List[HeatmapData] = Field(..., description="热力图数据列表")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {"date": "2025-11-26", "count": 5, "level": 2},
                        {"date": "2025-11-25", "count": 3, "level": 1},
                        {"date": "2025-11-24", "count": 0, "level": 0}
                    ]
                }
            ]
        }
    }


class ActivitySummary(BaseModel):
    """活动统计摘要"""
    total_days: int = Field(..., description="总活跃天数")
    total_activities: int = Field(..., description="总活动次数")
    current_streak: int = Field(..., description="当前连续天数")
    longest_streak: int = Field(..., description="最长连续天数")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_days": 30,
                    "total_activities": 150,
                    "current_streak": 7,
                    "longest_streak": 14
                }
            ]
        }
    }
