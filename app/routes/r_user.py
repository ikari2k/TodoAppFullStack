from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.db_user import (
    db_create_user,
    db_delete_user,
    db_read_user,
    db_read_users,
    db_update_user,
)
from app.db.models import DBUser
from app.exceptions import NotFoundException
from app.schemas import User, UserCreate, UserUpdate


router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not Found"}}
)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int = Path(gt=0), db: Session = Depends(get_db)
) -> User:
    try:
        return db_read_user(user_id, db)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)) -> List[User]:
    return db_read_users(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    check_if_user_exists(user, db)
    return db_create_user(user, db)


def check_if_user_exists(user, db):
    existing_email = db.query(DBUser).filter(DBUser.email == user.email).first()
    existing_username = (
        db.query(DBUser).filter(DBUser.username == user.username).first()
    )

    if existing_email or existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with existing email or username does already exist",
        )


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int, user: UserUpdate, db: Session = Depends(get_db)
) -> User:
    check_if_user_exists(user, db)
    try:
        return db_update_user(user_id, user, db)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    try:
        return db_delete_user(user_id, db)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
