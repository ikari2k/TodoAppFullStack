import sys

sys.path.append("..")

from fastapi.testclient import TestClient
from fastapi import status

from app.main import appTodo
from app.db.models import DBUser


client = TestClient(appTodo)


def test_get_user_by_id(test_user: DBUser):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
