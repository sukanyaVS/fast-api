from sqlalchemy.exc import IntegrityError

from fastapi_project.models import UserSkill
from fastapi_project.repositories import SkillRepository
from fastapi_project.schemas import SkillCreate


class DuplicateSkillError(Exception):
    pass


class SkillService:
    def __init__(self, skill_repository: SkillRepository) -> None:
        self.skill_repository = skill_repository

    async def create_skill(self, skill_data: SkillCreate):
        try:
            return await self.skill_repository.create(skill_data)
        except IntegrityError as error:
            raise DuplicateSkillError from error

    async def list_skills(self):
        return await self.skill_repository.get_all()

    async def assign_skill_to_user(self, user_id: int, skill_id: int, level: str | None = None):
        return await self.skill_repository.assign_to_user(user_id, skill_id, level)

    async def get_user_skills(self, user_id: int):
        return await self.skill_repository.get_user_skills(user_id)
