# main.py
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.manager import UserManagerDependency

from custom_verify import get_custom_verify_router
from db import User, fake_db
from schemas import CustomUserRead


# 用户管理器依赖
class UserManager(BaseUserManager[User, uuid.UUID]):
    def __init__(self):
        super().__init__(user_db=fake_db)  # 传入 fake_db


async def get_user_manager() -> UserManager:
    yield UserManager()


# FastAPI 用户实例
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [])  # 添加认证后端

app = FastAPI()

# 注册自定义验证路由
app.include_router(
    fastapi_users.get_custom_verify_router(get_user_manager, CustomUserRead),
    prefix="/auth",
    tags=["auth"],
)


if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
