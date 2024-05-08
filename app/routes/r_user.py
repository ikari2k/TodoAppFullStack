from fastapi import APIRouter, Depends, HTTPException, status, Path

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.db_user import db_read_user
from app.exceptions import NotFoundException


router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not Found"}}
)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    try:
        return db_read_user(user_id, db)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
