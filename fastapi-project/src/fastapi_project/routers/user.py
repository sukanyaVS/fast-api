from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_project.database import get_db
from fastapi_project.repositories import UserRepository
from fastapi_project.schemas import UserCreate, UserRead, UserUpdate, UserWithDepartment
from fastapi_project.services import DuplicateEmailError, UserService

router = APIRouter(prefix="/users", tags=["users"])
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


def get_user_service(db: DatabaseSession) -> UserService:
    return UserService(UserRepository(db))


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, service: UserServiceDependency) -> UserRead:
    try:
        return await service.create_user(user_data)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from None


@router.get("", response_model=list[UserRead])
async def list_users(
    service: UserServiceDependency,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[UserRead]:
    return await service.get_users(skip, limit)


@router.get("/{user_id}", response_model=UserWithDepartment)
async def get_user(user_id: int, service: UserServiceDependency) -> UserWithDepartment:
    user = await service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int, user_data: UserUpdate, service: UserServiceDependency
) -> UserRead:
    try:
        user = await service.update_user(user_id, user_data)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from None
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDependency) -> Response:
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)