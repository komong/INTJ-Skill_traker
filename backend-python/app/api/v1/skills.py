"""
技能管理相关API路由
处理技能数据的获取和更新请求
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.skill import SkillDataOut, SkillDataUpdate, SkillDataResponse
from app.schemas.common import ErrorResponse
from app.services import skill_service
from app.models.user import User
from app.utils.response import success_response, error_response

router = APIRouter()


@router.get(
    "",
    response_model=dict,
    summary="获取用户技能数据",
    responses={
        200: {"description": "获取成功"},
        404: {"model": ErrorResponse, "description": "数据不存在"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def get_skills(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的完整技能数据
    
    返回：
    - skills: 技能数据数组
    - lastModified: 最后修改时间
    - version: 数据版本号（用于后续更新时的冲突检测）
    """
    skill_data = await skill_service.get_skill_data(db, current_user.id)
    
    if not skill_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(
                code="SKILL_DATA_NOT_FOUND",
                message="技能数据不存在"
            )
        )
    
    # 构造响应（与Node.js版本一致）
    skill_out = SkillDataOut(
        skills=skill_data.skill_data,  # skill_data.skill_data 是数组
        last_modified=skill_data.last_modified,
        version=skill_data.version
    )
    
    return success_response(
        data=skill_out.model_dump(by_alias=True),
        message="获取成功"
    )


@router.put(
    "",
    response_model=dict,
    summary="更新用户技能数据",
    responses={
        200: {"description": "更新成功"},
        409: {"model": ErrorResponse, "description": "版本冲突"},
        400: {"model": ErrorResponse, "description": "请求数据无效"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def update_skills(
    update_data: SkillDataUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的技能数据
    
    参数：
    - skills: 新的技能数组
    - version: 当前版本号（用于冲突检测）
    
    版本冲突检测（乐观锁）：
    - 如果客户端版本号与服务器版本号不一致，返回409错误
    - 更新成功后版本号自动+1
    """
    try:
        updated_skill_data = await skill_service.update_skill_data(
            db,
            current_user.id,
            update_data.skills,  # 传递技能数组
            update_data.version
        )
        
        # 构造响应（与Node.js版本一致）
        skill_response = SkillDataResponse(
            version=updated_skill_data.version,
            message="保存成功"
        )
        
        return success_response(
            data=skill_response.model_dump(),
            message="保存成功"
        )
    
    except ValueError as e:
        error_msg = str(e)
        
        # 判断是版本冲突还是数据不存在
        if "版本冲突" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_response(
                    code="VERSION_CONFLICT",
                    message=error_msg
                )
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    code="SKILL_DATA_NOT_FOUND",
                    message=error_msg
                )
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                code="INTERNAL_ERROR",
                message="更新技能数据时发生错误"
            )
        )
