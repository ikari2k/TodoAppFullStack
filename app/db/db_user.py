from fastapi import Depends

from sqlalchemy.orm import Session

from db.database import get_db
from db.hash import Hash
from db.models import DBUser
from exceptions import NotFoundException
from schemas import User, UserCreate, UserRole, UserUpdate


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
    return db_user


def db_read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db_find_user(user_id, db)
    return User(**db_user.__dict__)


def db_update_user(
    user_id: int, user: UserUpdate, db: Session = Depends(get_db)
) -> User:
    db_user = db_find_user(user_id, db)
    db_user.email = user.email
    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.role = UserRole.STANDARD.value
    db_user.password = Hash.bcrypt(user.password)

    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)


def db_delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db_find_user(user_id, db)
    db.delete(db_user)
    db.commit()
    return User(**db_user.__dict__)
