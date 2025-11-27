"""
统一响应格式工具
确保API响应格式与Node.js版本保持一致
"""

from typing import Any, Optional, Dict


def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """
    创建成功响应
    
    Args:
        data: 响应数据
        message: 成功消息
        
    Returns:
        Dict[str, Any]: 标准格式的成功响应
    """
    return {
        "success": True,
        "data": data,
        "message": message
    }


def error_response(
    code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    创建错误响应
    
    Args:
        code: 错误码
        message: 错误消息
        details: 错误详情（可选）
        
    Returns:
        Dict[str, Any]: 标准格式的错误响应
    """
    error_obj = {
        "code": code,
        "message": message
    }
    
    if details:
        error_obj["details"] = details
    
    return {
        "success": False,
        "error": error_obj
    }
