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
