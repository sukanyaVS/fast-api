from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_project.models import Department, User, UserProfile
from fastapi_project.schemas import DepartmentCreate, UserCreate, UserProfileCreate


class DuplicateUserProfileError(Exception):
    pass


class RelationshipRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_department(self, department_data: DepartmentCreate) -> Department:
        department = Department(**department_data.model_dump())
        self.db.add(department)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(department)
        return department

    async def get_department(self, department_id: int) -> Department | None:
        result = await self.db.execute(
            select(Department)
            .options(selectinload(Department.users))
            .where(Department.id == department_id)
        )
        return result.scalar_one_or_none()

    async def create_department_user(
        self, department_id: int, user_data: UserCreate
    ) -> User | None:
        department = await self.db.get(Department, department_id)
        if department is None:
            return None
        user = User(**user_data.model_dump(), department=department)
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(user)
        return user

    async def create_user_profile(
        self, user_id: int, profile_data: UserProfileCreate
    ) -> UserProfile | None:
        user = await self.db.get(User, user_id)
        if user is None:
            return None
        profile = UserProfile(user=user, **profile_data.model_dump())
        self.db.add(profile)
        try:
            await self.db.commit()
        except IntegrityError as error:
            await self.db.rollback()
            raise DuplicateUserProfileError from error
        await self.db.refresh(profile)
        return profile

    async def get_user_profile(self, user_id: int) -> UserProfile | None:
        result = await self.db.scalars(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.one_or_none()