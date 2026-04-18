# 用户相关API路由

from config.db_conf import get_db
from crud import users
from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from utils import response

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

    """ return {
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
    } """
    response_data = UserAuthResponse(
        token=token, user_info=UserInfoResponse.model_validate(new_user)
    )
    return response.success_response(message="注册成功", data=response_data)


""" 
登录
请求方法： post
参数： Pydantic 类型
检查用户是否存在 → 不存在返回 None，存在验证用户和密码 → 生成token，返回响应结果
"""


# 用户登录
@router.post("/login")
async def login(
    user_data: UserRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await users.authenticate_user(db, user_data.username, user_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="用户不存在或密码错误")

    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(
        token=token, user_info=UserInfoResponse.model_validate(user)
    )
    return response.success_response(message="登录成功", data=response_data)
