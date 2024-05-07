from fastapi import FastAPI

from .db import models
from .db.database import engine
from .routes import r_user


appTodo = FastAPI()

models.Base.metadata.create_all(bind=engine)


@appTodo.get("/health_check")
def health_check():
    return {"status": "Healthy"}


appTodo.include_router(r_user.router)
