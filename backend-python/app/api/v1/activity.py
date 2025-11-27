"""
活动日志相关API路由
处理活动记录、热力图和统计数据请求
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.activity import ActivityCreate, ActivityOut, HeatmapResponse, ActivitySummary
from app.schemas.common import ErrorResponse
from app.services import activity_service
from app.models.user import User
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="记录活动",
    responses={
        201: {"description": "记录成功"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def log_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    记录用户活动
    
    - 如果当天已有记录，则增加活动计数
    - 如果当天无记录，则创建新记录
    """
    try:
        activity = await activity_service.log_activity(
            db,
            current_user.id,
            activity_data.details
        )
        
        activity_out = ActivityOut.model_validate(activity)
        
        return success_response(
            data=activity_out.model_dump(),
            message="活动记录成功"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                code="INTERNAL_ERROR",
                message="记录活动时发生错误"
            )
        )


@router.get(
    "/heatmap",
    response_model=dict,
    summary="获取热力图数据",
    responses={
        200: {"description": "获取成功"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def get_heatmap(
    days: int = Query(180, ge=1, le=365, description="查询天数范围"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户活动热力图数据
    
    返回指定天数范围内的活动数据，包括：
    - date: 日期
    - count: 活动次数
    - level: 热度等级（0-4）
    """
    try:
        heatmap_data = await activity_service.get_heatmap(
            db,
            current_user.id,
            days
        )
        
        heatmap_response = HeatmapResponse(data=heatmap_data)
        
        return success_response(
            data=heatmap_response.model_dump(),
            message="获取热力图数据成功"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                code="INTERNAL_ERROR",
                message="获取热力图数据时发生错误"
            )
        )


@router.get(
    "/summary",
    response_model=dict,
    summary="获取活动统计摘要",
    responses={
        200: {"description": "获取成功"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户活动统计摘要
    
    返回：
    - total_days: 总活跃天数
    - total_activities: 总活动次数
    - current_streak: 当前连续天数
    - longest_streak: 最长连续天数
    """
    try:
        summary = await activity_service.get_activity_summary(
            db,
            current_user.id
        )
        
        return success_response(
            data=summary.model_dump(),
            message="获取活动统计成功"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                code="INTERNAL_ERROR",
                message="获取活动统计时发生错误"
            )
        )
