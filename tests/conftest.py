from typing import Any, Generator
import pytest

from app.auth.authentication import get_current_user
from app.main import appTodo
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from fastapi.testclient import TestClient

from app.db.database import Base, get_db
from app.db.hash import Hash
from app.db.models import DBTodo, DBUser
from app.schemas import UserRole, UserTokenData

SQLALCHEMY_DB_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(appTodo)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return UserTokenData(username="admin", id=1, role=UserRole.ADMIN)


appTodo.dependency_overrides[get_db] = override_get_db
appTodo.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
def session() -> Generator[Session, None, None]:
    # Create tables in the test db
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()

    # Drop the tables in test db
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user() -> Generator[Any, Any, Any]:
    # Create tables in the test db
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    db_user = DBUser(
        email="admin@email.com",
        username="admin",
        first_name="admin",
        last_name="admin",
        role=UserRole.ADMIN.value,
        password=Hash.bcrypt("test1234!"),
        is_active=True,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    yield db_user, session

    session.close()

    # Drop the tables in test db
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_todo() -> Generator[Any, Any, Any]:
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    db_todo = DBTodo(
        title="Sample todo",
        description="Sample description",
        priority=3,
        completed=False,
        user_id=1,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    yield db_todo, session

    session.close()
    # Drop the tables in test db
    Base.metadata.drop_all(bind=engine)
