from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.db.db_user import db_create_user, db_find_user, db_read_user
from app.db.hash import Hash
from app.schemas import User, UserCreate


def test_create_user(session: Session) -> None:
    user = db_create_user(
        UserCreate(
            email="user@email.com",
            username="test_user",
            first_name="test",
            last_name="user",
            password="test1234",
        ),
        session,
    )
    assert user.username == "test_user"
    assert user.first_name == "test"
    assert user.last_name == "user"
    assert user.username == "test_user"
    assert Hash.verify("test1234", str.encode(user.password))


def test_find_user(session: Session) -> None:
    user = db_create_user(
        UserCreate(
            email="user@email.com",
            username="test_user",
            first_name="test",
            last_name="user",
            password="test1234",
        ),
        session,
    )

    user_id = user.id
    user_db = db_find_user(user_id, session)
    assert user_db.email == "user@email.com"
