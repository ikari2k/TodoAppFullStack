import pytest
from typing import List
from sqlalchemy.orm import Session

from app.db.db_todos import db_find_todo, db_find_todos, db_read_todo, db_read_todos
from app.db.models import DBTodo
from app.exceptions import NotFoundException
from app.schemas import Todo


def test_find_todos(test_todo: tuple[DBTodo, Session]):
    db_todo, session = test_todo
    todo = db_find_todos(session)
    assert type(todo) == list
    assert len(todo) == 1
    assert type(todo[0]) == DBTodo
    assert todo[0].title == db_todo.title
    assert todo[0].description == db_todo.description
    assert todo[0].completed == db_todo.completed
    assert todo[0].priority == db_todo.priority
    assert todo[0].user_id == db_todo.user_id


def test_read_todos(test_todo: tuple[DBTodo, Session]):
    db_todo, session = test_todo
    todo = db_read_todos(session)
    assert type(todo) == list
    assert len(todo) == 1
    assert type(todo[0]) == Todo
    assert todo[0].title == db_todo.title
    assert todo[0].description == db_todo.description
    assert todo[0].completed == db_todo.completed
    assert todo[0].priority == db_todo.priority
    assert todo[0].user_id == db_todo.user_id


def test_find_todo(test_todo: tuple[DBTodo, Session]):
    db_todo, session = test_todo
    todo = db_find_todo(db_todo.id, session)
    assert type(todo) == DBTodo
    assert todo.title == db_todo.title
    assert todo.description == db_todo.description
    assert todo.completed == db_todo.completed
    assert todo.priority == db_todo.priority
    assert todo.user_id == db_todo.user_id


def test_read_todo(test_todo: tuple[DBTodo, Session]):
    db_todo, session = test_todo
    todo = db_read_todo(db_todo.id, session)
    assert type(todo) == Todo
    assert todo.title == db_todo.title
    assert todo.description == db_todo.description
    assert todo.completed == db_todo.completed
    assert todo.priority == db_todo.priority
    assert todo.user_id == db_todo.user_id


def test_find_nonexisting_todo(test_todo: tuple[DBTodo, Session]):
    db_todo, session = test_todo
    with pytest.raises(NotFoundException):
        db_find_todo(999, session)


def test_read_nonexisting_todo(test_todo: tuple[DBTodo, Session]):
    db_todo, session = test_todo
    with pytest.raises(NotFoundException):
        db_read_todo(999, session)
