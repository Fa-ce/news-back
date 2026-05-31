from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# 新闻的模型类
class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishTime")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# Optional[str] = 可以是字符串，也可以为空
