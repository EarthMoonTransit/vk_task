import uuid
from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    title: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
