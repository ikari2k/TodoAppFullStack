import pytest

from fastapi.testclient import TestClient
from fastapi import HTTPException, status

from app.db.hash import Hash
from app.main import appTodo
from app.db.models import DBUser


client = TestClient(appTodo)


def test_get_user_by_id(test_user: DBUser):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["email"] == "admin@email.com"
    assert data["username"] == "admin"
    assert data["first_name"] == "admin"
    assert data["last_name"] == "admin"
    assert data["role"] == "admin"
    assert Hash.verify("test1234!", str.encode(data["password"]))


def test_get_nonexisting_user_by_id(test_user: DBUser):
    response = client.get(f"/users/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}
