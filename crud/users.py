# 用户相关数据库操作

import uuid
from datetime import datetime, timedelta

from models.users import User, UserToken
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils import security


# 异常类
class UserAlreadyExistsError(Exception):
    pass
    # def __init__(self, username: str):
    #     super().__init__(f"用户已存在: {username}")
    #     self.username = username


# 创建用户
async def create_user(db: AsyncSession, username: str, password: str) -> User:
    # 密码加密处理
    user = User(username=username, password=security.get_hash_password(password))
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError as exc:
        await db.rollback()
        raise UserAlreadyExistsError(username) from exc


# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 根据用户ID查询用户
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 查询所有用户
async def get_all_users(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


# 生成 Token
async def create_token(db: AsyncSession, user_id: int) -> str:
    # 生成令牌 + 设置过期时间 → 查询数据库当前用户是否有 Token → 有：更新 Token → 无：创建 Token
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token


# 验证用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user
