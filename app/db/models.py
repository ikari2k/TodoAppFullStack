import sys

sys.path.append("..")

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str]
