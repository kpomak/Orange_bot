from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from bot.config import ENGINE


class DBase:
    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = "user"
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(String(255))
        first_name: Mapped[Optional[str]]
        last_name: Mapped[Optional[str]]
        authors: Mapped[List[lambda: DBase.Author]] = relationship(
            back_populates="user", cascade="all, delete-orphan"
        )

        def __repr__(self) -> str:
            return f"User(id={self.id}, username={self.username})"

    class Author(Base):
        __tablename__ = "authors"
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(String(127))
        subscripter: Mapped[int] = mapped_column(ForeignKey("user.id"))
        user: Mapped[lambda: DBase.User] = relationship(back_populates="authors")
        repos: Mapped[List[lambda: DBase.Repo]] = relationship(
            back_populates="author", cascade="all, delete-orphan"
        )

        def __repr__(self) -> str:
            return f"Author(id={self.id}, username={self.username})"

    class Repo(Base):
        __tablename__ = "repositories"
        id: Mapped[int] = mapped_column(primary_key=True)
        owner: Mapped[lambda: DBase.Author] = mapped_column(ForeignKey("authors.id"))
        name: Mapped[str]
        url: Mapped[str]
        updated_at: Mapped[datetime]
        author: Mapped[lambda: DBase.Author] = relationship(back_populates="repos")

        def __repr__(self) -> str:
            return f"Repo(name={self.name}, updated={self.updated_at})"

    def __init__(self) -> None:
        self.engine = create_engine(**ENGINE)
        self.Base.metadata.create_all(self.engine)

    def add_user(self, kwargs):
        with Session(self.engine) as session:
            user = session.execute(
                select(self.User).where(self.User.id == kwargs.get("id"))
            ).first()
            if not user:
                user = self.User(
                    id=kwargs.get("id"),
                    username=kwargs.get("username"),
                    first_name=kwargs.get("first_name"),
                    last_name=kwargs.get("last_name"),
                )
                session.add(user)
                session.commit()


if __name__ == "__main__":
    db = DBase()
    roman = {
        "id": 207,
        "first_name": "Рома",
        "last_name": None,
        "username": "Roma_Ryzhkov",
        "type": "private",
    }
    db.add_user(roman)
