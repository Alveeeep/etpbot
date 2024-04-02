from sqlalchemy import BIGINT, BOOLEAN
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BIGINT, nullable=False)


class User(Base):
    __tablename__ = 'users'


class Admin(Base):
    __tablename__ = 'admins'
