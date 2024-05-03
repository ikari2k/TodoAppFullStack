from fastapi import FastAPI

from app.db import models
from app.db.database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/health_check")
def health_check():
    return {"status": "Healthy"}
