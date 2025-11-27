"""
通用响应格式Schemas
定义标准的成功和错误响应格式
"""

from typing import TypeVar, Generic, Optional, Dict, Any
from pydantic import BaseModel, Field

# 泛型类型变量
T = TypeVar('T')


class ErrorDetail(BaseModel):
    """错误详情"""
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详细信息")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "INVALID_CREDENTIALS",
                    "message": "用户名或密码错误",
                    "details": None
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = Field(False, description="请求是否成功")
    error: ErrorDetail = Field(..., description="错误信息")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "用户名或密码错误"
                    }
                }
            ]
        }
    }


class SuccessResponse(BaseModel, Generic[T]):
    """成功响应（泛型）"""
    success: bool = Field(True, description="请求是否成功")
    data: T = Field(..., description="响应数据")
    message: str = Field("Success", description="成功消息")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "data": {"id": 1, "username": "johndoe"},
                    "message": "Success"
                }
            ]
        }
    }


class MessageResponse(BaseModel):
    """纯消息响应"""
    success: bool = Field(True, description="请求是否成功")
    message: str = Field(..., description="消息内容")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "message": "操作成功"
                }
            ]
        }
    }


class PaginationMeta(BaseModel):
    """分页元信息"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total": 100,
                    "page": 1,
                    "page_size": 20,
                    "total_pages": 5
                }
            ]
        }
    }


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应（泛型）"""
    success: bool = Field(True, description="请求是否成功")
    data: list[T] = Field(..., description="数据列表")
    meta: PaginationMeta = Field(..., description="分页信息")
    message: str = Field("Success", description="成功消息")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "data": [{"id": 1}, {"id": 2}],
                    "meta": {
                        "total": 100,
                        "page": 1,
                        "page_size": 20,
                        "total_pages": 5
                    },
                    "message": "Success"
                }
            ]
        }
    }
