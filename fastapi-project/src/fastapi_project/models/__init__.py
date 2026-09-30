from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
	pass


from fastapi_project.models.user import User

__all__ = ["Base", "User"]
