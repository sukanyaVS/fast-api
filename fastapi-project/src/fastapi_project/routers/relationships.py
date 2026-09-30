from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.database import get_db
from fastapi_project.repositories import (
    DuplicateUserProfileError,
    RelationshipRepository,
)
from fastapi_project.schemas import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentWithUsers,
    UserCreate,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
)

router = APIRouter(tags=["relationships"])
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/departments",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    department_data: DepartmentCreate, db: DatabaseSession
) -> DepartmentRead:
    try:
        return await RelationshipRepository(db).create_department(department_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A department with this name already exists",
        ) from None


@router.get("/departments/{department_id}", response_model=DepartmentWithUsers)
async def get_department(
    department_id: int, db: DatabaseSession
) -> DepartmentWithUsers:
    department = await RelationshipRepository(db).get_department(department_id)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    return department


@router.post(
    "/departments/{department_id}/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_department_user(
    department_id: int, user_data: UserCreate, db: DatabaseSession
) -> UserRead:
    try:
        user = await RelationshipRepository(db).create_department_user(
            department_id, user_data
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    return user


@router.post(
    "/users/{user_id}/profile",
    response_model=UserProfileRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_profile(
    user_id: int, profile_data: UserProfileCreate, db: DatabaseSession
) -> UserProfileRead:
    try:
        profile = await RelationshipRepository(db).create_user_profile(
            user_id, profile_data
        )
    except DuplicateUserProfileError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already has a profile",
        ) from None
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return profile


@router.get("/users/{user_id}/profile", response_model=UserProfileRead)
async def get_user_profile(user_id: int, db: DatabaseSession) -> UserProfileRead:
    profile = await RelationshipRepository(db).get_user_profile(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        )
    return profile