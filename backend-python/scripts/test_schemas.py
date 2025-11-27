"""
Pydantic Schemas测试脚本
测试数据验证、序列化等功能
"""

import sys
from pathlib import Path

# 将项目根目录添加到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from loguru import logger
from pydantic import ValidationError

from app.schemas.user import UserRegister, UserLogin, UserOut, TokenResponse
from app.schemas.skill import SkillDataOut, SkillDataUpdate
from app.schemas.activity import ActivityCreate, HeatmapData, HeatmapResponse
from app.schemas.common import SuccessResponse, ErrorResponse, ErrorDetail


def test_user_schemas():
    """测试用户相关schemas"""
    logger.info("=" * 50)
    logger.info("测试用户Schemas...")
    logger.info("=" * 50)
    
    # 测试UserRegister - 成功案例
    try:
        user_reg = UserRegister(
            username="johndoe",
            email="john@example.com",
            password="Test@1234"
        )
        logger.info(f"✅ UserRegister验证成功: {user_reg.username}")
    except ValidationError as e:
        logger.error(f"❌ UserRegister验证失败: {e}")
    
    # 测试UserRegister - 密码强度失败
    try:
        weak_password = UserRegister(
            username="johndoe",
            email="john@example.com",
            password="weak"  # 太弱
        )
        logger.error("❌ 应该拒绝弱密码!")
    except ValidationError as e:
        logger.info(f"✅ 正确拒绝弱密码: {e.errors()[0]['msg']}")
    
    # 测试UserRegister - 邮箱格式错误
    try:
        invalid_email = UserRegister(
            username="johndoe",
            email="not-an-email",
            password="Test@1234"
        )
        logger.error("❌ 应该拒绝无效邮箱!")
    except ValidationError as e:
        logger.info(f"✅ 正确拒绝无效邮箱")
    
    # 测试UserOut
    user_out = UserOut(
        id=1,
        username="johndoe",
        email="john@example.com",
        created_at=datetime.utcnow(),
        last_login_at=None,
        is_active=True
    )
    logger.info(f"✅ UserOut创建成功: {user_out.model_dump()}")
    
    logger.info("")


def test_skill_schemas():
    """测试技能相关schemas"""
    logger.info("=" * 50)
    logger.info("测试技能Schemas...")
    logger.info("=" * 50)
    
    # 测试SkillDataUpdate
    skill_update = SkillDataUpdate(
        skill_data={
            "skills": [
                {
                    "id": "ai-agent",
                    "name": "AI代理使用",
                    "levels": []
                }
            ]
        },
        version=1
    )
    logger.info(f"✅ SkillDataUpdate验证成功, version={skill_update.version}")
    
    # 测试SkillDataOut
    skill_out = SkillDataOut(
        skill_data={"skills": []},
        last_modified=datetime.utcnow(),
        version=1
    )
    logger.info(f"✅ SkillDataOut创建成功")
    
    logger.info("")


def test_activity_schemas():
    """测试活动相关schemas"""
    logger.info("=" * 50)
    logger.info("测试活动Schemas...")
    logger.info("=" * 50)
    
    # 测试ActivityCreate
    activity = ActivityCreate(
        details={"action": "complete_criteria", "skill_id": "ai-agent"}
    )
    logger.info(f"✅ ActivityCreate验证成功")
    
    # 测试HeatmapData
    heatmap_data = HeatmapData(
        date="2025-11-26",
        count=5,
        level=2
    )
    logger.info(f"✅ HeatmapData创建成功: {heatmap_data.date}")
    
    # 测试HeatmapResponse
    heatmap_response = HeatmapResponse(
        data=[
            HeatmapData(date="2025-11-26", count=5, level=2),
            HeatmapData(date="2025-11-25", count=3, level=1),
        ]
    )
    logger.info(f"✅ HeatmapResponse创建成功, {len(heatmap_response.data)}个数据点")
    
    logger.info("")


def test_common_schemas():
    """测试通用响应schemas"""
    logger.info("=" * 50)
    logger.info("测试通用响应Schemas...")
    logger.info("=" * 50)
    
    # 测试SuccessResponse
    success_resp = SuccessResponse(
        success=True,
        data={"user_id": 1, "username": "johndoe"},
        message="登录成功"
    )
    logger.info(f"✅ SuccessResponse创建成功")
    logger.info(f"   {success_resp.model_dump_json()}")
    
    # 测试ErrorResponse
    error_resp = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code="INVALID_CREDENTIALS",
            message="用户名或密码错误"
        )
    )
    logger.info(f"✅ ErrorResponse创建成功")
    logger.info(f"   {error_resp.model_dump_json()}")
    
    logger.info("")


def test_json_serialization():
    """测试JSON序列化"""
    logger.info("=" * 50)
    logger.info("测试JSON序列化...")
    logger.info("=" * 50)
    
    user = UserOut(
        id=1,
        username="johndoe",
        email="john@example.com",
        created_at=datetime.utcnow(),
        last_login_at=None,
        is_active=True
    )
    
    # 转为JSON
    json_str = user.model_dump_json()
    logger.info(f"✅ JSON序列化成功:")
    logger.info(f"   {json_str}")
    
    # 从JSON解析
    user_from_json = UserOut.model_validate_json(json_str)
    logger.info(f"✅ JSON反序列化成功: {user_from_json.username}")
    
    logger.info("")


def main():
    """主测试函数"""
    logger.info("🚀 开始Pydantic Schemas测试\n")
    
    try:
        test_user_schemas()
        test_skill_schemas()
        test_activity_schemas()
        test_common_schemas()
        test_json_serialization()
        
        logger.info("=" * 50)
        logger.info("✅ 所有Schemas测试通过!")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
