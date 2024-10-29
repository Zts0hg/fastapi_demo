# db.py
import uuid
from typing import Dict, Optional


class User:
    def __init__(
        self,
        email: str,
        username: str,
        is_active: bool = True,
        is_verified: bool = False,
    ):
        self.id: uuid.UUID = uuid.uuid4()
        self.email = email
        self.username = username
        self.is_active = is_active
        self.is_verified = is_verified


class UserDatabase:
    def __init__(self):
        self.users: Dict[uuid.UUID, User] = {}

    def create_user(self, email: str, username: str) -> User:
        user = User(email=email, username=username)
        self.users[user.id] = user
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None


fake_db = UserDatabase()  # 实例化用户数据库
