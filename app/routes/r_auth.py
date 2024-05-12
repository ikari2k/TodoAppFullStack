from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.authentication import authenticate_user, create_access_token
from app.db.database import get_db
from app.schemas import AccessToken

router = APIRouter(
    prefix="/auth", tags=["auth"], responses={404: {"description": "Not Found"}}
)


@router.post("/token", response_model=AccessToken)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
