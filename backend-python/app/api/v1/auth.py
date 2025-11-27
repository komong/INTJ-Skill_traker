"""
认证相关API路由
处理用户注册、登录、获取用户信息等请求
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.user import UserRegister, UserLogin, UserOut, TokenResponse
from app.schemas.common import ErrorResponse
from app.services import auth_service
from app.core.security import create_access_token
from app.models.user import User
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
    responses={
        201: {"description": "注册成功"},
        400: {"model": ErrorResponse, "description": "注册失败"},
    }
)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册
    
    - **username**: 用户名，3-50个字符
    - **email**: 邮箱地址
    - **password**: 密码，至少8位，包含大小写字母和数字
    """
    try:
        # 注册用户
        user = await auth_service.register_user(db, user_data)
        
        # 创建JWT token
        token = create_access_token({"user_id": user.id})
        
        # 构建响应
        user_out = UserOut.model_validate(user)
        token_response = TokenResponse(token=token, user=user_out)
        
        return success_response(
            data=token_response.model_dump(by_alias=True),
            message="注册成功"
        )
    
    except ValueError as e:
        # 用户名或邮箱已存在
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(
                code="REGISTRATION_FAILED",
                message=str(e)
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                code="INTERNAL_ERROR",
                message="注册过程中发生错误"
            )
        )


@router.post(
    "/login",
    response_model=dict,
    summary="用户登录",
    responses={
        200: {"description": "登录成功"},
        401: {"model": ErrorResponse, "description": "认证失败"},
    }
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录
    
    - **username_or_email**: 用户名或邮箱
    - **password**: 密码
    """
    # 验证用户
    user = await auth_service.authenticate_user(
        db,
        credentials.username_or_email,
        credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response(
                code="INVALID_CREDENTIALS",
                message="用户名或密码错误"
            )
        )
    
    # 创建JWT token
    token = create_access_token({"user_id": user.id})
    
    # 构建响应
    user_out = UserOut.model_validate(user)
    token_response = TokenResponse(token=token, user=user_out)
    
    return success_response(
        data=token_response.model_dump(by_alias=True),
        message="登录成功"
    )


@router.get(
    "/me",
    response_model=dict,
    summary="获取当前用户信息",
    responses={
        200: {"description": "获取成功"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户的信息
    
    需要在请求头中携带有效的JWT token:
    ```
    Authorization: Bearer <token>
    ```
    """
    user_out = UserOut.model_validate(current_user)
    
    return success_response(
        data=user_out.model_dump(by_alias=True),
        message="获取用户信息成功"
    )


@router.get(
    "/verify",
    response_model=dict,
    summary="验证Token（与Node.js版本兼容）",
    responses={
        200: {"description": "Token有效"},
        401: {"model": ErrorResponse, "description": "未授权"},
    }
)
async def verify_token(
    current_user: User = Depends(get_current_user)
):
    """
    验证JWT Token是否有效
    
    这个接口与Node.js版本的 /api/auth/verify 接口兼容
    """
    user_out = UserOut.model_validate(current_user)
    
    return success_response(
        data={"user": user_out.model_dump(by_alias=True)},
        message="Token 有效"
    )
