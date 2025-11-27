"""
技能相关的Pydantic Schemas
定义技能数据的输入输出格式
"""

from datetime import datetime
from typing import List, Any
from pydantic import BaseModel, Field


class SkillDataOut(BaseModel):
    """技能数据响应（与Node.js版本兼容）"""
    skills: List[Any] = Field(..., description="技能数据数组")
    last_modified: datetime = Field(..., description="最后修改时间", alias="lastModified")
    version: int = Field(..., description="数据版本号")
    
    model_config = {
        "from_attributes": False,  # 不直接从ORM创建，需要转换
        "populate_by_name": True,  # 允许使用字段名或别名
        "json_schema_extra": {
            "examples": [
                {
                    "skills": [
                        {
                            "id": "ai-agent-usage",
                            "name": "AI代理使用",
                            "levels": [
                                {
                                    "lvl": 1,
                                    "title": "入门者",
                                    "criteria": [
                                        {"id": "1", "text": "了解AI代理的基本概念", "done": True}
                                    ]
                                }
                            ]
                        }
                    ],
                    "lastModified": "2025-11-26T12:00:00Z",
                    "version": 1
                }
            ]
        }
    }


class SkillDataUpdate(BaseModel):
    """技能数据更新请求（与Node.js版本兼容）"""
    skills: List[Any] = Field(..., description="新的技能数组")
    version: int = Field(..., description="当前版本号（用于冲突检测）")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "skills": [
                        {
                            "id": "ai-agent-usage",
                            "name": "AI代理使用",
                            "levels": [
                                {
                                    "lvl": 1,
                                    "criteria": [
                                        {"id": "1", "text": "了解AI代理", "done": True}
                                    ]
                                }
                            ]
                        }
                    ],
                    "version": 1
                }
            ]
        }
    }


class SkillDataResponse(BaseModel):
    """技能数据更新响应（简化版）"""
    version: int = Field(..., description="新版本号")
    message: str = Field(default="保存成功", description="消息")
    
    model_config = {
        "from_attributes": False,
        "json_schema_extra": {
            "examples": [
                {
                    "version": 2,
                    "message": "保存成功"
                }
            ]
        }
    }
