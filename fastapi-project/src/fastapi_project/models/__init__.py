from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
	pass


from fastapi_project.models.department import Department
from fastapi_project.models.user import User
from fastapi_project.models.user_profile import UserProfile

__all__ = ["Base", "Department", "User", "UserProfile"]
