from pydantic import BaseModel, ConfigDict, Field


class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class SkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class UserSkillAssign(BaseModel):
    skill_id: int
    level: str | None = Field(default=None, max_length=20)


class UserSkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    skill_id: int
    level: str | None


class UserWithSkills(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skills: list[SkillRead]
