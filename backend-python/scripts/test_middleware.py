"""
中间件测试脚本
测试CORS、请求日志、错误处理等中间件功能
"""

import requests
import json
from loguru import logger

BASE_URL = "http://127.0.0.1:8000"

# 禁用代理
proxies = {
    "http": None,
    "https": None,
}


def test_cors():
    """测试CORS中间件"""
    logger.info("=" * 60)
    logger.info("测试 CORS 中间件")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/health"
    headers = {
        "Origin": "http://localhost:3000"
    }
    
    logger.info(f"GET {url}")
    logger.info(f"Origin: {headers['Origin']}")
    
    response = requests.get(url, headers=headers, proxies=proxies)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"CORS Headers:")
    logger.info(f"  Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'N/A')}")
    logger.info(f"  Access-Control-Allow-Credentials: {response.headers.get('access-control-allow-credentials', 'N/A')}")
    
    if "access-control-allow-origin" in response.headers:
        logger.info("✅ CORS中间件工作正常!")
    else:
        logger.warning("⚠️ 未检测到CORS响应头")
    
    logger.info("")


def test_validation_error():
    """测试请求验证错误处理"""
    logger.info("=" * 60)
    logger.info("测试 请求验证错误处理")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/register"
    
    # 发送错误的数据（密码太短）
    payload = {
        "username": "test",
        "email": "invalid-email",  # 无效邮箱
        "password": "123"  # 密码太短
    }
    
    logger.info(f"POST {url}")
    logger.info(f"Payload (invalid): {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload, proxies=proxies)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 422:
        data = response.json()
        logger.info(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if not data.get("success"):
            logger.info("✅ 验证错误处理正常!")
        else:
            logger.error("❌ 验证错误处理异常!")
    else:
        logger.error(f"❌ 期望状态码422，实际: {response.status_code}")
    
    logger.info("")


def test_404_error():
    """测试404错误处理"""
    logger.info("=" * 60)
    logger.info("测试 404错误处理")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/nonexistent"
    
    logger.info(f"GET {url}")
    
    response = requests.get(url, proxies=proxies)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 404:
        data = response.json()
        logger.info(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if not data.get("success"):
            logger.info("✅ 404错误处理正常!")
        else:
            logger.error("❌ 404错误处理异常!")
    else:
        logger.error(f"❌ 期望状态码404，实际: {response.status_code}")
    
    logger.info("")


def test_request_logging():
    """测试请求日志中间件"""
    logger.info("=" * 60)
    logger.info("测试 请求日志中间件")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/health"
    
    logger.info(f"GET {url}")
    logger.info("提示: 检查服务器日志，应该能看到请求ID和处理时间")
    
    response = requests.get(url, proxies=proxies)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {response.json()}")
    logger.info("✅ 请求已发送，请查看服务器终端日志")
    
    logger.info("")


def test_auth_error():
    """测试认证错误处理"""
    logger.info("=" * 60)
    logger.info("测试 认证错误处理")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": "Bearer invalid-token"
    }
    
    logger.info(f"GET {url}")
    logger.info("Authorization: Bearer invalid-token")
    
    response = requests.get(url, headers=headers, proxies=proxies)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 401:
        data = response.json()
        logger.info(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        logger.info("✅ 认证错误处理正常!")
    else:
        logger.error(f"❌ 期望状态码401，实际: {response.status_code}")
    
    logger.info("")


def main():
    """运行所有中间件测试"""
    logger.info("╔" + "═" * 58 + "╗")
    logger.info("║" + " " * 15 + "中间件功能测试" + " " * 29 + "║")
    logger.info("╚" + "═" * 58 + "╝")
    logger.info("")
    
    test_cors()
    test_request_logging()
    test_validation_error()
    test_404_error()
    test_auth_error()
    
    logger.info("=" * 60)
    logger.info("🎉 所有中间件测试完成!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
