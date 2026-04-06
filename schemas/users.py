# 用户数据验证模型
from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str
