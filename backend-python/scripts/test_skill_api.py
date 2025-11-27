"""
技能管理API测试脚本
测试获取和更新技能数据接口，包括版本冲突检测
"""

import requests
import json
from loguru import logger

BASE_URL = "http://127.0.0.1:8001"


def get_auth_token():
    """获取认证token"""
    url = f"{BASE_URL}/api/auth/login"
    payload = {
        "username_or_email": "testuser2",
        "password": "Test@1234"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["token"]
    else:
        logger.error("登录失败，无法获取token")
        return None


def test_get_skills(token: str):
    """测试获取技能数据"""
    logger.info("=" * 60)
    logger.info("测试获取技能数据 API")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/skills"
    headers = {"Authorization": f"Bearer {token}"}
    
    logger.info(f"GET {url}")
    
    response = requests.get(url, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 获取技能数据成功!")
            skill_info = data["data"]
            logger.info(f"   Version: {skill_info['version']}")
            logger.info(f"   Last Modified: {skill_info.get('lastModified', skill_info.get('last_modified'))}")
            logger.info(f"   Skills Count: {len(skill_info['skills'])}")
            return skill_info
        else:
            logger.error("❌ 获取失败!")
            return None
    else:
        logger.error(f"❌ 获取失败! 状态码: {response.status_code}")
        return None


def test_update_skills_success(token: str, current_version: int):
    """测试成功更新技能数据"""
    logger.info("\n" + "=" * 60)
    logger.info("测试更新技能数据 API (正常更新)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/skills"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 构造新的技能数据
    payload = {
        "skills": [
            {
                "id": "python-backend",
                "name": "Python后端开发",
                "levels": [
                    {
                        "lvl": 1,
                        "title": "入门",
                        "criteria": [
                            {"id": "1", "text": "掌握FastAPI框架", "done": True}
                        ]
                    }
                ]
            }
        ],
        "version": current_version
    }
    
    logger.info(f"PUT {url}")
    logger.info(f"Payload version: {payload['version']}")
    
    response = requests.put(url, json=payload, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 更新技能数据成功!")
            updated_info = data["data"]
            logger.info(f"   New Version: {updated_info['version']}")
            logger.info(f"   Message: {updated_info.get('message', '')}")
            return updated_info["version"]
        else:
            logger.error("❌ 更新失败!")
            return None
    else:
        logger.error(f"❌ 更新失败! 状态码: {response.status_code}")
        return None


def test_update_skills_conflict(token: str, wrong_version: int):
    """测试版本冲突（使用错误的版本号）"""
    logger.info("\n" + "=" * 60)
    logger.info("测试版本冲突检测 (应该返回409)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/skills"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "skills": [
            {
                "id": "test",
                "name": "测试技能"
            }
        ],
        "version": wrong_version
    }
    
    logger.info(f"PUT {url}")
    logger.info(f"Payload version (错误): {payload['version']}")
    
    response = requests.put(url, json=payload, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 409:
        logger.info("✅ 正确检测到版本冲突!")
    else:
        logger.error("❌ 应该返回409状态码!")


def test_get_skills_without_token():
    """测试不带token获取技能数据"""
    logger.info("\n" + "=" * 60)
    logger.info("测试不带Token获取技能数据 (应该失败)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/skills"
    
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
    logger.info("🚀 开始技能管理API测试\n")
    
    try:
        # 1. 获取token
        token = get_auth_token()
        if not token:
            logger.error("无法获取认证token，测试终止")
            return
        
        # 2. 获取当前技能数据
        skill_info = test_get_skills(token)
        if not skill_info:
            logger.error("无法获取技能数据，测试终止")
            return
        
        current_version = skill_info["version"]
        
        # 3. 测试成功更新
        new_version = test_update_skills_success(token, current_version)
        
        # 4. 测试版本冲突（使用旧版本号）
        if new_version:
            test_update_skills_conflict(token, current_version)
        
        # 5. 测试无token访问
        test_get_skills_without_token()
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 所有技能管理API测试完成!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
