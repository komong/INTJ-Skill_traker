"""
CORS中间件配置
处理跨域请求
"""

from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def setup_cors(app):
    """
    配置CORS中间件
    
    Args:
        app: FastAPI应用实例
    """
    # 允许的源
    origins = [
        "http://localhost:3000",  # React开发服务器
        "http://localhost:5173",  # Vite开发服务器
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # 如果有生产环境域名，从配置中添加
    # if settings.FRONTEND_URL:
    #     origins.append(settings.FRONTEND_URL)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 允许的源列表
        allow_credentials=True,  # 允许携带凭证（cookies等）
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有请求头
    )
