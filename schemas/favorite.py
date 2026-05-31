# 收藏数据验证模型
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from schemas.base import NewsItemBase


class FavoriteCheckResponseBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    is_favorite: bool = Field(..., description="是否收藏", alias="isFavorite")


# 添加收藏的请求提类型
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., description="新闻ID", alias="newsId")


# 规划两个类： 新闻模型类 + 收藏的模型类
# 定义收藏的模型类
class FavoriteResponseBase(NewsItemBase):
    # 继承 NewsItemBase 新闻模型类
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    favorite_id: int = Field(..., description="收藏ID", alias="favoriteId")
    favorite_time: datetime = Field(..., description="收藏时间", alias="favoriteTime")


# 收藏列表接口响应模型类
class FavoriteListResponseBase(BaseModel):
    list: list[FavoriteResponseBase]
    total: int
    has_more: bool = Field(..., description="是否还有更多", alias="hasMore")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    # pydantic 模型的配置，populate_by_name=True 表示允许用原始字段名或者别名来赋值；from_attributes=True 表示允许从 ORM 对象属性中取值,而不仅仅是字典
    # 这两个配置让模型更灵活，可以接受： - 字典形式的数据（前端发来的 JSON） - 对象形式的数据（数据库返回的 ORM 对象） - 用驼峰命名（hasMore）或蛇形命名（has_more）都行；这样代码就不用手动转换和映射字段名了。
