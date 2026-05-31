# 收藏相关API路由
from config.db_conf import get_db
from crud import favorite
from fastapi import APIRouter, Query
from fastapi.params import Depends
from models.users import User
from schemas.favorite import (
    FavoriteAddRequest,
    FavoriteCheckResponseBase,
    FavoriteListResponseBase,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import auth, response

router = APIRouter()


# 检查收藏状态
@router.get("/check")
async def check_favorite(
    db: AsyncSession = Depends(get_db),
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(auth.get_current_user),
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)
    return response.success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckResponseBase(is_favorite=is_favorite),
    )


# 添加收藏
@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth.get_current_user),
):
    is_favorite = await favorite.is_news_favorite(db, user.id, data.news_id)
    if is_favorite:
        return response.success_response(message="已收藏")
    result = await favorite.add_news_favorite(db, user_id=user.id, news_id=data.news_id)
    return response.success_response(message="添加收藏成功", data=result)


# 取消收藏
@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth.get_current_user),
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    return response.success_response(message="取消收藏成功", data=result)


# 获取收藏列表
@router.get("/list")
async def get_favorite_list(
    page: int = Query(default=1, description="请输入页码"),
    page_size: int = Query(default=10, description="请输入分页大小", alias="pageSize"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth.get_current_user),
):
    rows, total = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [
        {
            **news.__dict__,  # news.__dict__ —— 把 news 对象的所有属性转成字典
            "favoriteTime": favorite_time,
            "favoriteId": favorite_id,
        }  # {**...} —— 字典解包符，把一个字典的内容展开到新字典里；后面的 "favoriteTime": favorite_time 等，是新增或覆盖的字段
        for news, favorite_time, favorite_id in rows
    ]
    has_more = (page - 1) * page_size + len(favorite_list) < total
    data = FavoriteListResponseBase(
        list=favorite_list,
        total=total,
        has_more=has_more,
    )
    return response.success_response(
        message="获取收藏列表成功",
        data=data,
    )


# 清空收藏列表
@router.delete("/clear")
async def clear_favorite_list(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth.get_current_user),
):
    result = await favorite.clear_favorite_list(db, user.id)
    return response.success_response(message=f"成功删除{result}条收藏记录")
