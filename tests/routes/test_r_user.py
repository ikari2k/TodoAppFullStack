import pytest
import json

from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy.orm import Session

from app.db.hash import Hash
from app.main import appTodo
from app.db.models import DBUser
from app.schemas import UserCreate, UserRole


client = TestClient(appTodo)


def test_get_user_by_id(test_user: DBUser):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username
    assert data["first_name"] == test_user.first_name
    assert data["last_name"] == test_user.last_name
    assert data["role"] == test_user.role


def test_get_nonexisting_user_by_id(test_user: DBUser):
    response = client.get("/users/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_create_user(session: Session):
    user = UserCreate(
        email="new_email1@email.com",
        username="new_user1",
        first_name="new_FN",
        last_name="new_LN",
        password="new_password",
    )

    data = json.dumps(user.__dict__)
    response = client.post("/users/", json=json.loads(data))
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data["email"] == user.email
    assert response_data["username"] == user.username
    assert response_data["first_name"] == user.first_name
    assert response_data["last_name"] == user.last_name
    assert response_data["role"] == UserRole.STANDARD.value

    db_user = session.query(DBUser).filter(DBUser.id == 2).first()
    assert db_user
    assert db_user.email == user.email
    assert db_user.first_name == user.first_name
    assert db_user.last_name == user.last_name
    assert db_user.username == user.username
    assert Hash.verify(user.password, db_user.password)


def test_create_invalid_user_same_email(session: Session):
    user1 = UserCreate(
        email="new_email@email.com",
        username="new_user1",
        first_name="new_FN1",
        last_name="new_LN1",
        password="new_password1",
    )
    user2 = UserCreate(
        email="new_email@email.com",
        username="new_user2",
        first_name="new_FN2",
        last_name="new_LN2",
        password="new_password2",
    )

    data_user1 = json.dumps(user1.__dict__)
    response = client.post("/users/", json=json.loads(data_user1))
    assert response.status_code == status.HTTP_201_CREATED

    data_user2 = json.dumps(user2.__dict__)
    response = client.post("/users/", json=json.loads(data_user2))
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_invalid_user_same_username(session: Session):
    user1 = UserCreate(
        email="new_email@email1.com",
        username="new_user",
        first_name="new_FN1",
        last_name="new_LN1",
        password="new_password1",
    )
    user2 = UserCreate(
        email="new_email@email2.com",
        username="new_user",
        first_name="new_FN2",
        last_name="new_LN2",
        password="new_password2",
    )

    data_user1 = json.dumps(user1.__dict__)
    response = client.post("/users/", json=json.loads(data_user1))
    assert response.status_code == status.HTTP_201_CREATED

    data_user2 = json.dumps(user2.__dict__)
    response = client.post("/users/", json=json.loads(data_user2))
    assert response.status_code == status.HTTP_409_CONFLICT
