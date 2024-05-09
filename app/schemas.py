from enum import Enum
from pydantic import BaseModel


class UserRole(Enum):
    ADMIN = "admin"
    STANDARD = "standard"


class User(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: UserRole


class UserCreate(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str


class UserUpdate(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
