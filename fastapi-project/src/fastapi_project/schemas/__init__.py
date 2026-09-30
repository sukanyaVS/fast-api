from fastapi_project.schemas.relationships import (
	DepartmentCreate,
	DepartmentRead,
	DepartmentWithUsers,
	UserProfileCreate,
	UserProfileRead,
	UserWithDepartment,
)
from fastapi_project.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
	"DepartmentCreate",
	"DepartmentRead",
	"DepartmentWithUsers",
	"UserCreate",
	"UserProfileCreate",
	"UserProfileRead",
	"UserRead",
	"UserUpdate",
	"UserWithDepartment",
]
