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


class PasswordVerification(BaseModel):
    current_password_to_verify: str
    new_password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class UserTokenData(BaseModel):
    username: str
    id: int
    role: UserRole


class Todo(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    user_id: int
    completed: bool
