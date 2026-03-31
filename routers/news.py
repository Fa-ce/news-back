# 新闻相关API路由

from config.db_conf import get_db
from crud import news
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# 获取新闻分类列表
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


# 获取新闻列表
@router.get("/list")
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    category_id: int = Query(..., description="请输入分类ID", alias="categoryId"),
    page: int = Query(default=1, description="请输入页码"),
    page_size: int = Query(default=10, description="请输入分页大小", alias="pageSize"),
):
    # 思路：处理分页规则 → 查询新闻列表 → 计算总量 → 计算是否还有更多
    skip = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, skip, page_size)
    total = await news.get_new_count(db, category_id)
    hasMore = skip + len(news_list) < total
    return {
        "code": 200,
        "msg": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": hasMore,
        },
    }
