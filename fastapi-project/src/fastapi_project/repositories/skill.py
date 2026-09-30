from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_project.models import Skill, User, UserSkill
from fastapi_project.schemas import SkillCreate


class DuplicateSkillError(Exception):
    pass


class SkillRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, skill_data: SkillCreate) -> Skill:
        skill = Skill(**skill_data.model_dump())
        self.db.add(skill)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(skill)
        return skill

    async def get_all(self) -> list[Skill]:
        result = await self.db.scalars(select(Skill).order_by(Skill.id))
        return list(result)

    async def get_by_id(self, skill_id: int) -> Skill | None:
        result = await self.db.scalars(
            select(Skill).where(Skill.id == skill_id).options(selectinload(Skill.users))
        )
        return result.one_or_none()

    async def assign_to_user(
        self, user_id: int, skill_id: int, level: str | None = None
    ) -> UserSkill | None:
        user = await self.db.get(User, user_id)
        if user is None:
            return None

        skill = await self.db.get(Skill, skill_id)
        if skill is None:
            return None

        existing = await self.db.get(UserSkill, {"user_id": user_id, "skill_id": skill_id})
        if existing is not None:
            existing.level = level
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        user_skill = UserSkill(user=user, skill=skill, level=level)
        self.db.add(user_skill)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(user_skill)
        return user_skill

    async def get_user_skills(self, user_id: int) -> list[Skill]:
        result = await self.db.scalars(
            select(Skill)
            .join(UserSkill, Skill.id == UserSkill.skill_id)
            .where(UserSkill.user_id == user_id)
            .order_by(Skill.id)
        )
        return list(result)
