from fastapi_project.routers.relationships import router as relationships_router
from fastapi_project.routers.skill import router as skill_router
from fastapi_project.routers.user import router as user_router

__all__ = ["relationships_router", "skill_router", "user_router"]
