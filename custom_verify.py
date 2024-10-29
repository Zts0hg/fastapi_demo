# custom_verify.py
import uuid
from typing import Type

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi_users import exceptions, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency


def get_custom_verify_router(
    get_user_manager: UserManagerDependency[
        schemas.U, uuid.UUID
    ],  # 更新 ID 为 uuid.UUID
    user_schema: Type[schemas.U],
):
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
            get_user_manager
        ),  # 更新 ID 为 uuid.UUID
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
