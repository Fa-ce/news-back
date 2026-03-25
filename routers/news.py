# 新闻相关API路由

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news

router = APIRouter()


@router.get("/categories")
async def get_categories(
    skip: int = Query(default=0, description="请输入页码"),
    limit: int = Query(default=100, description="请输入分页大小"),
    # skip: int = 0,
    # limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "msg": "获取分类成功",
        "data": categories,
    }
