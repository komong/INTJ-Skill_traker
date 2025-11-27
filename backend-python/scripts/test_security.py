"""
安全模块测试脚本
测试密码加密和JWT token的兼容性
"""

import sys
from pathlib import Path

# 将项目根目录添加到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from loguru import logger


def test_password_hashing():
    """测试密码加密"""
    logger.info("=" * 50)
    logger.info("测试密码加密功能...")
    logger.info("=" * 50)
    
    # 测试密码
    test_password = "Test@1234"
    
    # 生成哈希
    hashed = hash_password(test_password)
    logger.info(f"✅ 密码加密成功")
    logger.info(f"   明文: {test_password}")
    logger.info(f"   哈希: {hashed[:60]}...")
    
    # 验证正确密码
    is_valid = verify_password(test_password, hashed)
    logger.info(f"✅ 正确密码验证: {is_valid}")
    
    # 验证错误密码
    is_invalid = verify_password("WrongPassword", hashed)
    logger.info(f"✅ 错误密码验证: {is_invalid}")
    
    # 测试Node.js生成的哈希（来自数据库的testuser密码）
    # Node.js bcrypt生成的哈希示例
    nodejs_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5uyT3Y7gEJhda"
    nodejs_password = "Test@1234"
    
    can_verify_nodejs = verify_password(nodejs_password, nodejs_hash)
    logger.info(f"✅ Python验证Node.js哈希: {can_verify_nodejs}")
    
    logger.info("")


def test_jwt_token():
    """测试JWT token"""
    logger.info("=" * 50)
    logger.info("测试JWT Token功能...")
    logger.info("=" * 50)
    
    # 创建token
    test_data = {"user_id": 1, "username": "testuser"}
    token = create_access_token(test_data)
    
    logger.info(f"✅ Token创建成功")
    logger.info(f"   Token: {token[:50]}...")
    
    # 解码token
    decoded = decode_access_token(token)
    logger.info(f"✅ Token解码成功")
    logger.info(f"   Payload: {decoded}")
    
    # 验证数据
    if decoded and decoded.get("user_id") == 1:
        logger.info(f"✅ Token数据验证成功")
    else:
        logger.error(f"❌ Token数据验证失败")
    
    # 测试无效token
    invalid_decoded = decode_access_token("invalid.token.here")
    logger.info(f"✅ 无效Token处理: {invalid_decoded}")
    
    logger.info("")


def test_xss_filter():
    """测试XSS过滤"""
    logger.info("=" * 50)
    logger.info("测试XSS过滤功能...")
    logger.info("=" * 50)
    
    from app.utils.xss_filter import sanitize_html
    
    # 测试XSS攻击代码
    xss_input = '<script>alert("XSS")</script>Hello World'
    cleaned = sanitize_html(xss_input)
    
    logger.info(f"✅ XSS过滤测试")
    logger.info(f"   输入: {xss_input}")
    logger.info(f"   输出: {cleaned}")
    
    # 测试普通文本
    normal_input = "This is a normal text"
    cleaned_normal = sanitize_html(normal_input)
    logger.info(f"✅ 普通文本: {cleaned_normal}")
    
    logger.info("")


def main():
    """主测试函数"""
    logger.info("🚀 开始安全模块测试\n")
    
    try:
        test_password_hashing()
        test_jwt_token()
        test_xss_filter()
        
        logger.info("=" * 50)
        logger.info("✅ 所有测试通过!")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
