# 收藏相关数据库操作
from models.favorite import Favorite
from models.news import News
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession


# 检查收藏状态： 当前用户是否收藏了该新闻
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    query = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


# 添加收藏
async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 取消收藏
async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    # 1. 查询当前用户是否收藏了该新闻
    query = delete(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


# 获取收藏列表
async def get_favorite_list(
    db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10
):
    # 获取某用户的收藏列表、分页功能 总量 + 收藏的新闻列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()
    offset = (page - 1) * page_size
    # 获取收藏列表 - 联表查询 join() + 收藏时间排序 + 分页
    query = (
        select(
            News,
            Favorite.created_at.label("favorite_time"),  # 给两个表的重复字段起别名
            Favorite.id.label("favorite_id"),  # 给两个表的重复字段起别名
        )
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# 清空收藏列表
async def clear_favorite_list(db: AsyncSession, user_id: int):
    query = delete(Favorite).where(Favorite.user_id == user_id)  # 清空当前用户的收藏
    result = await db.execute(query)
    await db.commit()
    # 返回删除的数量
    return result.rowcount or 0
