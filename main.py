# 应用入口文件

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api_router

app = FastAPI()

# 注册路由
app.include_router(api_router)

# 允许跨域请求地址
CORS_URLS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://192.168.1.99:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_URLS,  # 允许的源，开发阶段可以设置为 "*"，生产环境可以设置为具体的域名
    allow_credentials=True,  # 允许携带 cookie
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)
