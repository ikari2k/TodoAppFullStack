from sqlalchemy.orm import Session

from app.db.db_user import db_create_user, db_read_user
from app.schemas import UserCreate


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
