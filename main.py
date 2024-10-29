# main.py
import uuid
from typing import Generic, Type, TypeVar

import uvicorn
from fastapi import APIRouter, Body, Depends, FastAPI, Request, status
from fastapi_users import BaseUserManager, FastAPIUsers, exceptions, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency

from db import User, fake_db
from schemas import CustomUserRead

U = TypeVar("U", bound=schemas.BaseUser)
ID = TypeVar("ID")


# 用户管理器依赖
class UserManager(BaseUserManager[User, uuid.UUID]):
    def __init__(self):
        super().__init__(user_db=fake_db)  # 传入 fake_db


async def get_user_manager() -> UserManager:
    yield UserManager()


# 创建自定义用户管理类
class CustomFastAPIUsers(FastAPIUsers[U, ID], Generic[U, ID]):
    def get_verify_router(self, user_schema: Type[schemas.U]):
        router = APIRouter()

        @router.post(
            "/request-verify-token",
            status_code=status.HTTP_202_ACCEPTED,
            name="verify:request-token",
        )
        async def request_verify_token(
            request: Request,
            email: str = Body(..., embed=True),  # 修改为 str 类型
            user_manager: BaseUserManager[schemas.U, uuid.UUID] = Depends(
                self.get_user_manager
            ),  # 使用实例属性
        ):
            try:
                user = await user_manager.get_by_email(email)
                await user_manager.request_verify(user)
            except (
                exceptions.UserNotExists,
                exceptions.UserInactive,
                exceptions.UserAlreadyVerified,
            ):
                pass

            return None

        return router


# FastAPI 用户实例
fastapi_users = CustomFastAPIUsers[User, uuid.UUID](
    get_user_manager, []
)  # 添加认证后端

app = FastAPI()

# 注册自定义验证路由
app.include_router(
    fastapi_users.get_verify_router(CustomUserRead),
    prefix="/auth",
    tags=["auth"],
)


if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
