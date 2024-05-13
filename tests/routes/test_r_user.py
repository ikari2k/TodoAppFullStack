import pytest
import json

from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy.orm import Session

from app.db.db_user import db_find_user
from app.db.hash import Hash
from app.main import appTodo
from app.db.models import DBUser
from app.schemas import PasswordVerification, UserCreate, UserRole, UserUpdate


client = TestClient(appTodo)


def test_get_user_by_id(test_user: tuple[DBUser, Session]):
    db_user, session = test_user
    response = client.get(f"/users/{db_user.id}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["email"] == db_user.email
    assert data["username"] == db_user.username
    assert data["first_name"] == db_user.first_name
    assert data["last_name"] == db_user.last_name
    assert data["role"] == db_user.role


def test_get_current_user(test_user: tuple[DBUser, Session]):
    db_user, session = test_user
    response = client.get("/users/current/")
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["id"] == db_user.id
    assert user_data["username"] == db_user.username
    assert user_data["email"] == db_user.email
    assert user_data["first_name"] == db_user.first_name
    assert user_data["last_name"] == db_user.last_name
    assert user_data["role"] == db_user.role


def test_get_nonexisting_user_by_id(session: Session):
    response = client.get("/users/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_all_users(test_user: tuple[DBUser, Session]):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1


def test_create_valid_user(session: Session):
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

    user_id = response_data["id"]

    db_user = session.query(DBUser).filter(DBUser.id == user_id).first()
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


def test_update_valid_user(session: Session):
    user_to_update = UserCreate(
        email="new_email1@email.com",
        username="new_user1",
        first_name="new_FN",
        last_name="new_LN",
        password="new_password",
    )

    data_to_update = json.dumps(user_to_update.__dict__)
    response = client.post("/users/", json=json.loads(data_to_update))
    assert response.status_code == status.HTTP_201_CREATED

    id_to_update = response.json()["id"]

    user_updated = UserUpdate(
        email="updated@email.com",
        username="updated",
        first_name="updated_FN",
        last_name="updated_LN",
        password="updated_password",
    )

    data_updated = json.dumps(user_updated.__dict__)

    response = client.put(f"/users/{id_to_update}", json=json.loads(data_updated))
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["email"] == user_updated.email
    assert response_data["username"] == user_updated.username
    assert response_data["first_name"] == user_updated.first_name
    assert response_data["last_name"] == user_updated.last_name
    assert response_data["role"] == UserRole.STANDARD.value

    db_user = session.query(DBUser).filter(DBUser.id == id_to_update).first()
    assert db_user
    assert db_user.email == user_updated.email
    assert db_user.first_name == user_updated.first_name
    assert db_user.last_name == user_updated.last_name
    assert db_user.username == user_updated.username
    assert Hash.verify(user_updated.password, db_user.password)


def test_update_invalid_user(session: Session):
    user_updated = UserUpdate(
        email="updated@email.com",
        username="updated",
        first_name="updated_FN",
        last_name="updated_LN",
        password="updated_password",
    )

    data_updated = json.dumps(user_updated.__dict__)

    response = client.put(f"/users/999", json=json.loads(data_updated))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_change_password(test_user: tuple[DBUser, Session]):
    password_verification = PasswordVerification(
        current_password_to_verify="test1234!", new_password="new_password"
    )
    password_verification_json = json.dumps(password_verification.__dict__)
    response = client.put(
        "/users/password/", json=json.loads(password_verification_json)
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_valid_user(test_user: tuple[DBUser, Session]):
    db_user, session = test_user
    response = client.delete(f"/users/{db_user.id}")
    assert response.status_code == status.HTTP_200_OK, response.text

    response_get = client.get(f"/users/{db_user.id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_user(session: Session):
    response = client.delete(f"/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
