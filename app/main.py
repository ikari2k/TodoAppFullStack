from fastapi import FastAPI

from app.db import models
from app.db.database import engine
from app.routes import r_user


appTodo = FastAPI()

models.Base.metadata.create_all(bind=engine)


@appTodo.get("/health_check")
def health_check():
    return {"status": "Healthy"}


appTodo.include_router(r_user.router)
