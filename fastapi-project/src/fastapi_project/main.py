from fastapi import FastAPI

from fastapi_project.routers import relationships_router, skill_router, user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(relationships_router)
app.include_router(skill_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
