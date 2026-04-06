# 用户相关API路由

from config.db_conf import get_db
from crud import users
from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserRequest
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# 用户注册
@router.post("/register")
async def register(db: AsyncSession = Depends(get_db), user: UserRequest = None):
    # 注册逻辑：验证用户是否存在 → 创建用户 → 生成Token → 返回响应结果
    # 先判断用户是否存在
    # 创建用户
    try:
        new_user = await users.create_user(db, user.username, user.password)
        token = await users.create_token(db, new_user.id)
    except users.UserAlreadyExistsError:
        raise HTTPException(status_code=200, detail="用户已存在")

    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": new_user.id,
                "username": new_user.username,
                "bio": new_user.bio,
                "avatar": new_user.avatar,
            },
        },
    }
