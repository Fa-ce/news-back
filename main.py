# 应用入口文件

from fastapi import FastAPI
from routers import api_router


app = FastAPI()

# 注册路由
app.include_router(api_router)
