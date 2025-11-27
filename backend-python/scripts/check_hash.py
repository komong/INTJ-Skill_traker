"""获取数据库中的用户密码哈希"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from sqlalchemy import select
from app.core.database import async_session_factory
from app.models.user import User
from app.core.security import verify_password

async def test_real_hash():
    try:
        async with async_session_factory() as session:
            result = await session.execute(select(User).where(User.username == 'testuser2'))
            user = result.scalar_one_or_none()
            if user:
                print(f"Username: {user.username}")
                print(f"Hash from DB: {user.password_hash}")
                
                # 测试常见密码
                test_passwords = ["Test@1234", "test123", "root", "testuser2"]
                for pwd in test_passwords:
                    is_match = verify_password(pwd, user.password_hash)
                    print(f"Testing '{pwd}': {is_match}")
            else:
                print("User not found")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_real_hash())
