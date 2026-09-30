from pydantic import BaseModel, ConfigDict, Field

from fastapi_project.schemas.user import UserRead


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class DepartmentWithUsers(DepartmentRead):
    users: list[UserRead]


class UserProfileCreate(BaseModel):
    bio: str | None = Field(default=None, max_length=500)


class UserProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    bio: str | None