from datetime import timedelta
from fastapi import HTTPException, status
import pytest
from sqlalchemy.orm import Session
from jose import jwt

from app.auth.authentication import (
    authenticate_user,
    create_access_token,
    get_current_user,
    secret_key,
    alg,
)
from app.db.models import DBUser
from app.schemas import UserRole


def test_authenticate_user(test_user: tuple[DBUser, Session]) -> None:
    db_user, session = test_user
    authenticated_user = authenticate_user(db_user.username, "test1234!", session)
    assert authenticated_user is not None
    assert authenticated_user.username == db_user.username


def test_authenticate_user_non_existent(session: Session):
    with pytest.raises(ValueError):
        authenticate_user("WrongUserNAme", "password", session)


def test_authenticate_user_wrong_password(test_user: tuple[DBUser, Session]):
    db_user, session = test_user
    with pytest.raises(ValueError):
        authenticate_user(db_user.username, "wrong_pass", session)


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(
        token, secret_key, algorithms=[alg], options={"verify_signature": False}
    )
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": UserRole.ADMIN.value}
    token = jwt.encode(encode, secret_key, algorithm=alg)
    user = get_current_user(token)

    assert user.id == 1
    assert user.username == "testuser"
    assert user.role == UserRole.ADMIN


def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, secret_key, algorithm=alg)
    with pytest.raises(HTTPException) as e:
        get_current_user(token)

    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate user"
