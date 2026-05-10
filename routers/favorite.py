# 收藏相关API路由
from crud import favorite
from fastapi import APIRouter, Header, HTTPException, Query
from fastapi.params import Depends
from models.users import User
from schemas.favorite import FavoriteCheckResponseBase
from sqlalchemy.ext.asyncio import AsyncSession
from utils import auth, response

router = APIRouter()


# 检查收藏状态
@router.get("/check")
async def check_favorite(
    db: AsyncSession = Depends(auth.get_db),
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(auth.get_current_user),
    Authorization: str = Header(default=..., alias="Authorization"),
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)
    if not is_favorite:
        raise HTTPException(status_code=404, detail="文章不存在")
    return response.success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckResponseBase(is_favorite=is_favorite),
    )
