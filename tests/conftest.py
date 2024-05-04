from typing import Generator
import pytest
import sys


sys.path.append("..")

from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base, get_db
from app.db.hash import Hash
from app.db.models import DBUser
from app.schemas import UserCreate, UserRole

SQLALCHEMY_DB_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def session() -> Generator[Session, None, None]:
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

    yield session

    session.close()

    # Drop the tables in test db
    Base.metadata.drop_all(bind=engine)
