import uuid
from datetime import datetime
from app.core.helpers import Env, Domain
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    login: EmailStr
    password: str


class UserCreate(UserBase, extra="allow"):
    model_config = {
        "json_schema_extra": {
            "examples": [{"login": "user@example.com", "password": "string"}]
        }
    }


class User(BaseModel):
    model_config = ConfigDict(strict=True)
    id: uuid.UUID
    created_at: datetime
    login: EmailStr
    env: Env
    domain: Domain
    locktime: datetime
