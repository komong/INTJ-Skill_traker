"""
认证API测试脚本
测试注册、登录、获取用户信息等接口
"""

import requests
import json
from loguru import logger

BASE_URL = "http://127.0.0.1:8001"


def test_register():
    """测试用户注册"""
    logger.info("=" * 60)
    logger.info("测试用户注册 API")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/register"
    payload = {
        "username": "testuser999",
        "email": "testuser999@example.com",
        "password": "Test@1234"
    }
    
    logger.info(f"POST {url}")
    logger.info(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 注册成功!")
            token = data["data"]["token"]
            user = data["data"]["user"]
            logger.info(f"   Token: {token[:50]}...")
            logger.info(f"   User: {user['username']} (ID: {user['id']})")
            return token
        else:
            logger.error("❌ 注册失败!")
            return None
    else:
        logger.error(f"❌ 注册失败! 状态码: {response.status_code}")
        return None


def test_login():
    """测试用户登录"""
    logger.info("\n" + "=" * 60)
    logger.info("测试用户登录 API")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/login"
    
    # 测试用数据库中已有的用户
    payload = {
        "username_or_email": "testuser2",
        "password": "Test@1234"
    }
    
    logger.info(f"POST {url}")
    logger.info(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 登录成功!")
            token = data["data"]["token"]
            user = data["data"]["user"]
            logger.info(f"   Token: {token[:50]}...")
            logger.info(f"   User: {user['username']} (ID: {user['id']})")
            return token
        else:
            logger.error("❌ 登录失败!")
            return None
    else:
        logger.error(f"❌ 登录失败! 状态码: {response.status_code}")
        return None


def test_login_with_wrong_password():
    """测试错误密码登录"""
    logger.info("\n" + "=" * 60)
    logger.info("测试错误密码登录 (应该失败)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/login"
    payload = {
        "username_or_email": "testuser2",
        "password": "WrongPassword123"
    }
    
    logger.info(f"POST {url}")
    logger.info(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 401:
        logger.info("✅ 正确拒绝了错误密码!")
    else:
        logger.error("❌ 应该返回401状态码!")


def test_get_current_user(token: str):
    """测试获取当前用户信息"""
    logger.info("\n" + "=" * 60)
    logger.info("测试获取当前用户信息 API")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    logger.info(f"GET {url}")
    logger.info(f"Headers: Authorization: Bearer {token[:30]}...")
    
    response = requests.get(url, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 获取用户信息成功!")
            user = data["data"]
            logger.info(f"   User: {user['username']} ({user['email']})")
            logger.info(f"   Created: {user.get('createdAt', user.get('created_at'))}")
            logger.info(f"   Active: {user.get('isActive', user.get('is_active'))}")
        else:
            logger.error("❌ 获取用户信息失败!")
    else:
        logger.error(f"❌ 获取用户信息失败! 状态码: {response.status_code}")


def test_get_current_user_without_token():
    """测试不带token获取用户信息"""
    logger.info("\n" + "=" * 60)
    logger.info("测试不带Token获取用户信息 (应该失败)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/auth/me"
    
    logger.info(f"GET {url}")
    logger.info("Headers: (无Authorization)")
    
    response = requests.get(url)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 401:
        logger.info("✅ 正确拒绝了无Token请求!")
    else:
        logger.error("❌ 应该返回401状态码!")


def main():
    """主测试函数"""
    logger.info("🚀 开始认证API测试\n")
    
    try:
        # 1. 测试登录（使用数据库已有用户）
        token = test_login()
        
        if token:
            # 2. 测试获取用户信息
            test_get_current_user(token)
        
        # 3. 测试错误密码登录
        test_login_with_wrong_password()
        
        # 4. 测试不带token获取用户信息
        test_get_current_user_without_token()
        
        # 5. 测试注册（可选，如果需要新用户）
        # new_token = test_register()
        # if new_token:
        #     test_get_current_user(new_token)
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 所有认证API测试完成!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
