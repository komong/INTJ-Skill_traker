"""
活动日志服务层
处理活动记录、热力图数据和统计摘要
"""

from datetime import datetime, date, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from loguru import logger

from app.models.activity_log import ActivityLog
from app.schemas.activity import HeatmapData, ActivitySummary


async def log_activity(
    db: AsyncSession,
    user_id: int,
    details: Optional[dict] = None
) -> ActivityLog:
    """
    记录用户活动
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        details: 活动详情（可选）
        
    Returns:
        ActivityLog: 活动记录对象
    """
    today = date.today()
    
    # 查询今天是否已有记录
    result = await db.execute(
        select(ActivityLog).where(
            and_(
                ActivityLog.user_id == user_id,
                ActivityLog.activity_date == today
            )
        )
    )
    activity = result.scalar_one_or_none()
    
    if activity:
        # 更新现有记录
        activity.activity_count += 1
        if details:
            # 合并details（可根据需求调整策略）
            if activity.details:
                activity.details = {**activity.details, **details}
            else:
                activity.details = details
    else:
        # 创建新记录
        activity = ActivityLog(
            user_id=user_id,
            activity_date=today,
            activity_count=1,
            details=details
        )
        db.add(activity)
    
    await db.commit()
    await db.refresh(activity)
    
    logger.info(f"活动记录成功: user_id={user_id}, date={today}, count={activity.activity_count}")
    
    return activity


async def get_heatmap(
    db: AsyncSession,
    user_id: int,
    range_days: int = 180
) -> List[HeatmapData]:
    """
    获取热力图数据
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        range_days: 查询天数范围（默认180天）
        
    Returns:
        List[HeatmapData]: 热力图数据列表
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=range_days - 1)
    
    # 查询指定时间范围内的活动记录
    result = await db.execute(
        select(ActivityLog).where(
            and_(
                ActivityLog.user_id == user_id,
                ActivityLog.activity_date >= start_date,
                ActivityLog.activity_date <= end_date
            )
        ).order_by(ActivityLog.activity_date)
    )
    activities = result.scalars().all()
    
    # 构建日期到活动计数的映射
    activity_map = {act.activity_date: act.activity_count for act in activities}
    
    # 生成完整的日期范围（包含无活动的日期）
    heatmap_data = []
    current_date = start_date
    
    while current_date <= end_date:
        count = activity_map.get(current_date, 0)
        level = calculate_heat_level(count)
        
        heatmap_data.append(
            HeatmapData(
                date=current_date.isoformat(),
                count=count,
                level=level
            )
        )
        
        current_date += timedelta(days=1)
    
    logger.info(f"热力图数据获取成功: user_id={user_id}, days={range_days}, total={len(heatmap_data)}")
    
    return heatmap_data


def calculate_heat_level(count: int) -> int:
    """
    根据活动次数计算热度等级
    
    Args:
        count: 活动次数
        
    Returns:
        int: 热度等级（0-4）
    """
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    elif count <= 5:
        return 2
    elif count <= 10:
        return 3
    else:
        return 4


async def get_activity_summary(
    db: AsyncSession,
    user_id: int
) -> ActivitySummary:
    """
    获取活动统计摘要
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        ActivitySummary: 活动统计摘要
    """
    # 查询所有活动记录
    result = await db.execute(
        select(ActivityLog).where(
            ActivityLog.user_id == user_id
        ).order_by(ActivityLog.activity_date)
    )
    activities = result.scalars().all()
    
    if not activities:
        return ActivitySummary(
            total_days=0,
            total_activities=0,
            current_streak=0,
            longest_streak=0
        )
    
    # 统计总天数和总活动次数
    total_days = len(activities)
    total_activities = sum(act.activity_count for act in activities)
    
    # 计算连续天数
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # 按日期排序（倒序）
    sorted_activities = sorted(activities, key=lambda x: x.activity_date, reverse=True)
    
    # 计算当前连续天数
    if sorted_activities[0].activity_date == today:
        current_streak = 1
        last_date = today
    elif sorted_activities[0].activity_date == yesterday:
        current_streak = 1
        last_date = yesterday
    else:
        current_streak = 0
        last_date = None
    
    if last_date:
        for act in sorted_activities[1:]:
            expected_date = last_date - timedelta(days=1)
            if act.activity_date == expected_date:
                current_streak += 1
                last_date = act.activity_date
            else:
                break
    
    # 计算最长连续天数
    for i, act in enumerate(sorted_activities):
        if i == 0:
            temp_streak = 1
            last_date = act.activity_date
        else:
            expected_date = last_date - timedelta(days=1)
            if act.activity_date == expected_date:
                temp_streak += 1
                last_date = act.activity_date
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
                last_date = act.activity_date
    
    longest_streak = max(longest_streak, temp_streak)
    
    logger.info(
        f"活动统计获取成功: user_id={user_id}, "
        f"total_days={total_days}, current_streak={current_streak}"
    )
    
    return ActivitySummary(
        total_days=total_days,
        total_activities=total_activities,
        current_streak=current_streak,
        longest_streak=longest_streak
    )
