from sqlalchemy.exc import IntegrityError

from fastapi_project.models import User
from fastapi_project.repositories import UserRepository
from fastapi_project.schemas import UserCreate, UserUpdate


class DuplicateEmailError(Exception):
    pass


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> User:
        try:
            return await self.user_repository.create(user_data)
        except IntegrityError as error:
            raise DuplicateEmailError from error

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repository.get_all(skip, limit)

    async def get_user(self, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def update_user(
        self, user_id: int, user_data: UserUpdate
    ) -> User | None:
        try:
            return await self.user_repository.update(user_id, user_data)
        except IntegrityError as error:
            raise DuplicateEmailError from error

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)