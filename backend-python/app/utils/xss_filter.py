"""
XSS过滤工具
防止跨站脚本攻击
"""

import bleach
from typing import Optional


# 允许的HTML标签（如果需要支持富文本）
ALLOWED_TAGS = []  # 暂不允许任何HTML标签

# 允许的HTML属性
ALLOWED_ATTRIBUTES = {}


def sanitize_html(text: Optional[str]) -> Optional[str]:
    """
    清理HTML内容，移除潜在的XSS攻击代码
    
    Args:
        text: 待清理的文本
        
    Returns:
        Optional[str]: 清理后的文本
    """
    if text is None:
        return None
    
    if not isinstance(text, str):
        return text
    
    # 使用bleach清理HTML
    cleaned = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True  # 移除不允许的标签
    )
    
    return cleaned


def sanitize_dict(data: dict) -> dict:
    """
    递归清理字典中的所有字符串值
    
    Args:
        data: 待清理的字典
        
    Returns:
        dict: 清理后的字典
    """
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned[key] = sanitize_html(value)
        elif isinstance(value, dict):
            cleaned[key] = sanitize_dict(value)
        elif isinstance(value, list):
            cleaned[key] = [
                sanitize_html(item) if isinstance(item, str)
                else sanitize_dict(item) if isinstance(item, dict)
                else item
                for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned
