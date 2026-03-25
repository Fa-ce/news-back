from fastapi import APIRouter

# 引入模块路由
from routers.news import router as news_router

# 创建 APIRouter 实例
api_router = APIRouter(prefix="/api")


# 注册各模块路由
api_router.include_router(news_router, prefix="/news", tags=["新闻"])
