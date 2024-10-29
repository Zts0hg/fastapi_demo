# schemas.py
import uuid

from fastapi_users import schemas


class CustomUserRead(schemas.BaseUser[uuid.UUID]):
    email: str
