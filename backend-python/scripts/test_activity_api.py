"""
活动日志API测试脚本
测试活动记录、热力图和统计摘要接口
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


def test_log_activity(token: str):
    """测试记录活动"""
    logger.info("=" * 60)
    logger.info("测试记录活动 API")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/activity"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "details": {
            "action": "complete_criteria",
            "skill_id": "python-backend",
            "timestamp": "2025-11-27T12:00:00Z"
        }
    }
    
    logger.info(f"POST {url}")
    logger.info(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 记录活动成功!")
            activity = data["data"]
            logger.info(f"   Date: {activity['activity_date']}")
            logger.info(f"   Count: {activity['activity_count']}")
        else:
            logger.error("❌ 记录失败!")
    else:
        logger.error(f"❌ 记录失败! 状态码: {response.status_code}")


def test_log_activity_multiple(token: str, times: int = 3):
    """测试多次记录活动"""
    logger.info("\n" + "=" * 60)
    logger.info(f"测试多次记录活动 ({times}次)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/activity"
    headers = {"Authorization": f"Bearer {token}"}
    
    for i in range(times):
        payload = {"details": {"action": f"test_{i+1}"}}
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            count = data["data"]["activity_count"]
            logger.info(f"   第{i+1}次记录成功, 当天总计: {count}次")
        else:
            logger.error(f"   第{i+1}次记录失败!")


def test_get_heatmap(token: str, days: int = 30):
    """测试获取热力图数据"""
    logger.info("\n" + "=" * 60)
    logger.info(f"测试获取热力图数据 (最近{days}天)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/activity/heatmap?days={days}"
    headers = {"Authorization": f"Bearer {token}"}
    
    logger.info(f"GET {url}")
    
    response = requests.get(url, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 获取热力图数据成功!")
            heatmap = data["data"]["data"]
            logger.info(f"   Total Days: {len(heatmap)}")
            
            # 显示有活动的日期
            active_days = [d for d in heatmap if d["count"] > 0]
            logger.info(f"   Active Days: {len(active_days)}")
            
            if active_days:
                logger.info("   最近活跃日期:")
                for day in active_days[-5:]:  # 显示最近5个活跃日
                    logger.info(f"     - {day['date']}: {day['count']}次 (Level {day['level']})")
        else:
            logger.error("❌ 获取失败!")
    else:
        logger.error(f"❌ 获取失败! 状态码: {response.status_code}")


def test_get_summary(token: str):
    """测试获取活动统计摘要"""
    logger.info("\n" + "=" * 60)
    logger.info("测试获取活动统计摘要 API")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/activity/summary"
    headers = {"Authorization": f"Bearer {token}"}
    
    logger.info(f"GET {url}")
    
    response = requests.get(url, headers=headers)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            logger.info("✅ 获取活动统计成功!")
            summary = data["data"]
            logger.info(f"   总活跃天数: {summary['total_days']}")
            logger.info(f"   总活动次数: {summary['total_activities']}")
            logger.info(f"   当前连续: {summary['current_streak']}天")
            logger.info(f"   最长连续: {summary['longest_streak']}天")
        else:
            logger.error("❌ 获取失败!")
    else:
        logger.error(f"❌ 获取失败! 状态码: {response.status_code}")


def test_without_token():
    """测试不带token访问"""
    logger.info("\n" + "=" * 60)
    logger.info("测试不带Token访问 (应该失败)")
    logger.info("=" * 60)
    
    url = f"{BASE_URL}/api/activity/summary"
    
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
    logger.info("🚀 开始活动日志API测试\n")
    
    try:
        # 1. 获取token
        token = get_auth_token()
        if not token:
            logger.error("无法获取认证token，测试终止")
            return
        
        # 2. 测试记录活动
        test_log_activity(token)
        
        # 3. 测试多次记录（增加计数）
        test_log_activity_multiple(token, 3)
        
        # 4. 测试获取热力图
        test_get_heatmap(token, 30)
        
        # 5. 测试获取统计摘要
        test_get_summary(token)
        
        # 6. 测试无token访问
        test_without_token()
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 所有活动日志API测试完成!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
