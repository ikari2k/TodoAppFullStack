from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy.orm import Session


from app.db.models import DBUser
from app.main import appTodo

client = TestClient(appTodo)


def test_create_token_for_valid_user(test_user: tuple[DBUser, Session]):
    db_user, session = test_user
    form_data = {"username": db_user.username, "password": "test1234!"}

    response = client.post("/auth/token", data=form_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_create_token_for_invalid_user(session: Session):
    form_data = {"username": "invalid_user", "password": "test1234!"}

    response = client.post("/auth/token", data=form_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_token_for_invalid_credentials(test_user: tuple[DBUser, Session]):
    db_user, session = test_user
    form_data = {"username": db_user.username, "password": "invalidPassword"}

    response = client.post("/auth/token", data=form_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
