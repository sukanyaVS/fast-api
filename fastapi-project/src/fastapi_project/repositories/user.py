from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi_project.models import User
from fastapi_project.schemas import UserCreate, UserUpdate
from fastapi_project.security import hash_password


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_data: UserCreate) -> User:
        user_values = user_data.model_dump(exclude={"password"})
        user = User(**user_values, password_hash=hash_password(user_data.password))
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.scalars(
            select(User)
            .options(joinedload(User.department))
            .where(User.id == user_id)
        )
        return result.one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.scalars(select(User).where(User.email == email))
        return result.one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.scalars(
            select(User).order_by(User.id).offset(skip).limit(limit)
        )
        return list(result)

    async def update(
        self, user_id: int, user_data: UserUpdate
    ) -> User | None:
        user = await self.get_by_id(user_id)
        if user is None:
            return None
        for field, value in user_data.model_dump().items():
            setattr(user, field, value)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user is None:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True