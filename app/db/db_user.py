from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.hash import Hash
from app.db.models import DBUser
from app.exceptions import NotFoundException
from app.schemas import User, UserCreate, UserRole, UserUpdate


def db_create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = DBUser(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=UserRole.STANDARD.value,
        password=Hash.bcrypt(user.password),
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return User(**db_user.__dict__)


def db_find_user(user_id: int, db: Session = Depends(get_db)) -> DBUser:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise NotFoundException("Item not found")
    return DBUser


def db_read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db_find_user(user_id, db)
    return User(**db_user.__dict__)


def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> User:
    db_user = db_find_user(user_id, db)
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)


def delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db_find_user(user_id, db)
    db.delete(db_user)
    db.commit()
    return User(**db_user.__dict__)
