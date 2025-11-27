"""
全局异常处理器
统一处理所有未捕获的异常
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from app.utils.response import error_response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    处理请求验证错误
    
    Args:
        request: 请求对象
        exc: 验证异常
        
    Returns:
        JSONResponse: 标准错误响应
    """
    errors = exc.errors()
    error_details = []
    
    for error in errors:
        error_details.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error: {error_details}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            code="VALIDATION_ERROR",
            message="请求数据验证失败",
            details={"errors": error_details}
        )
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    处理数据库异常
    
    Args:
        request: 请求对象
        exc: 数据库异常
        
    Returns:
        JSONResponse: 标准错误响应
    """
    logger.error(f"Database error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            code="DATABASE_ERROR",
            message="数据库操作失败"
        )
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    处理未捕获的通用异常
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSONResponse: 标准错误响应
    """
    logger.error(f"Unhandled exception: {type(exc).__name__} - {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            code="INTERNAL_SERVER_ERROR",
            message="服务器内部错误"
        )
    )


def setup_exception_handlers(app):
    """
    注册异常处理器
    
    Args:
        app: FastAPI应用实例
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
