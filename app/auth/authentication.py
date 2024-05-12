from datetime import timedelta, datetime
import os
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.hash import Hash
from app.db.models import DBUser
from app.schemas import UserRole, UserTokenData

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

load_dotenv()
if "SECRET_KEY" or "ALGORITHM" in os.environ:
    secret_key: str = os.getenv("SECRET_KEY")  # type: ignore
    alg: str = os.getenv("ALGORITHM")  # type: ignore


def create_access_token(
    username: str, user_id, role: str, expires_delta: timedelta
) -> str:
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, secret_key, algorithm=alg)


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> DBUser:
    db_user = db.query(DBUser).filter(DBUser.username == username).first()
    if not db_user:
        raise ValueError("User not found")
    if not Hash.verify(password, db_user.password):
        raise ValueError("Incorrect Password")
    return db_user


def get_current_user(token: str = Depends(oauth2_bearer)) -> UserTokenData:
    try:
        payload: dict[str, Any] = jwt.decode(token, secret_key, algorithms=alg)
        username: str = payload.get("sub")  # type: ignore
        user_id: int = payload.get("id")  # type: ignore
        user_role: UserRole = payload.get("role")  # type: ignore
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return UserTokenData(username=username, id=user_id, role=user_role)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
