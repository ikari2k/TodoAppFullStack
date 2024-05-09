import pytest

from sqlalchemy.orm import Session

from app.db.db_user import (
    db_create_user,
    db_delete_user,
    db_find_user,
    db_read_user,
    db_update_user,
)
from app.db.hash import Hash
from app.db.models import DBUser
from app.exceptions import NotFoundException
from app.schemas import UserCreate, UserUpdate


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
    assert user_db.username == "test_user"
    assert user_db.first_name == "test"
    assert user_db.last_name == "user"


def test_find_non_existing_user(session: Session) -> None:
    user_id = 999
    with pytest.raises(NotFoundException):
        db_find_user(user_id, session)


def test_read_user(test_user: tuple[DBUser, Session]) -> None:
    db_user, session = test_user
    user = db_read_user(db_user.id, session)
    assert user.email == "admin@email.com"
    assert user.username == "admin"
    assert user.first_name == "admin"
    assert user.last_name == "admin"


def test_update_user(test_user: tuple[DBUser, Session]) -> None:
    db_user, session = test_user
    user_id = db_user.id
    user_update = UserUpdate(
        email="admin_changed@email.com",
        username="admin_changed",
        first_name="admin_changed",
        last_name="admin_changed",
        password="password_changed",
    )
    db_update_user(user_id, user_update, session)

    user = db_read_user(1, session)
    assert user.email == "admin_changed@email.com"
    assert user.username == "admin_changed"
    assert user.first_name == "admin_changed"
    assert user.last_name == "admin_changed"


def test_delete_user(test_user: tuple[DBUser, Session]) -> None:
    db_user, session = test_user
    user_id = db_user.id
    db_delete_user(user_id, session)

    with pytest.raises(NotFoundException):
        db_find_user(user_id, session)
