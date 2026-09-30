from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.database import get_db
from fastapi_project.repositories import SkillRepository
from fastapi_project.schemas import (
    SkillCreate,
    SkillRead,
    UserSkillAssign,
    UserSkillRead,
    UserWithSkills,
)
from fastapi_project.services import DuplicateSkillError, SkillService
from fastapi_project.security import get_current_user

router = APIRouter(tags=["skills"], dependencies=[Depends(get_current_user)])
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


def get_skill_service(db: DatabaseSession) -> SkillService:
    return SkillService(SkillRepository(db))


SkillServiceDependency = Annotated[SkillService, Depends(get_skill_service)]


@router.post("/skills", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill_data: SkillCreate, service: SkillServiceDependency
) -> SkillRead:
    try:
        return await service.create_skill(skill_data)
    except DuplicateSkillError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A skill with this name already exists",
        ) from None


@router.get("/skills", response_model=list[SkillRead])
async def list_skills(service: SkillServiceDependency) -> list[SkillRead]:
    return await service.list_skills()


@router.post(
    "/users/{user_id}/skills",
    response_model=UserSkillRead,
    status_code=status.HTTP_201_CREATED,
)
async def assign_skill_to_user(
    user_id: int,
    assignment: UserSkillAssign,
    service: SkillServiceDependency,
) -> UserSkillRead:
    user_skill = await service.assign_skill_to_user(
        user_id, assignment.skill_id, assignment.level
    )
    if user_skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or skill not found",
        )
    return user_skill


@router.get("/users/{user_id}/skills", response_model=UserWithSkills)
async def get_user_skills(user_id: int, service: SkillServiceDependency) -> UserWithSkills:
    skills = await service.get_user_skills(user_id)
    return UserWithSkills(id=user_id, skills=skills)
