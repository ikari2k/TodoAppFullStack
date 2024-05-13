from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str]

    def __repr__(self) -> str:
        repr = (
            f"User(id={self.id}, name={self.username}, "
            f"fullname={self.first_name + self.last_name}), role={self.role}, "
            f"isActive={self.is_active}"
        )
        return repr


class DBTodo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    priority: Mapped[int]
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        repr = (
            f"Todo(id={self.id}, title={self.title}, "
            f"description={self.description}), priority={self.priority}, "
            f"isCompleted={self.completed}, user_id={self.user_id}"
        )
        return repr
