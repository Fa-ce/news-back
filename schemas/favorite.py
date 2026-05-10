# 收藏数据验证模型

from pydantic import BaseModel, Field


class FavoriteCheckResponseBase(BaseModel):
    is_favorite: bool = Field(..., description="是否收藏")
