from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import DBTodo
from app.exceptions import NotFoundException
from app.schemas import Todo


def db_find_todos(db: Session = Depends(get_db)) -> List[DBTodo]:
    return db.query(DBTodo).all()


def db_read_todos(db: Session = Depends(get_db)) -> List[Todo]:
    db_todos = db_find_todos(db)
    todos = []
    for t in db_todos:
        t = Todo(**t.__dict__)
        todos.append(t)
    return todos


def db_find_todo(todo_id: int, db: Session = Depends(get_db)) -> DBTodo:
    db_todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if db_todo is None:
        raise NotFoundException("Item not found")
    return db_todo


def db_read_todo(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    db_todo = db_find_todo(todo_id, db)
    return Todo(**db_todo.__dict__)
