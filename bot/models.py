from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import ENGINE
from git_api import get_authors_repos


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
        subscriber: Mapped[int] = mapped_column(ForeignKey("user.id"))
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

    def get_user(self, **kwargs):
        with Session(self.engine) as session:
            return session.get(self.User, kwargs.get("id"))

    # def get_author(self, **kwargs):
    #     with Session(self.engine) as session:
    #         author = session.execute(
    #             select(self.Author)
    #             .join(self.User.authors)
    #             .where(self.User.id == kwargs.get("id"))
    #             .where(self.Author.username == kwargs.get("author_username"))
    #         ).first()
    #         return author

    def add_user(self, **kwargs):
        with Session(self.engine) as session:
            user = self.get_user(**kwargs)
            if not user:
                user = self.User(
                    id=kwargs.get("id"),
                    username=kwargs.get("username"),
                    first_name=kwargs.get("first_name"),
                    last_name=kwargs.get("last_name"),
                )
                session.add(user)
                session.commit()

    def sudscribe_on_author(self, **kwargs):
        with Session(self.engine) as session:
            user = self.get_user(**kwargs)
            if not user:
                return

            author = self.Author(
                username=kwargs.get("author_username"),
                subscriber=user.id,
            )
            session.add(author)
            session.flush()

            repos = get_authors_repos(author.username)
            for item in repos:
                repo = self.Repo(
                    owner=author.id,
                    name=item.get("name"),
                    url=item.get("url"),
                    updated_at=item.get("updated_at"),
                )
                author.repos.append(repo)
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
    db.add_user(**roman)
    user = db.get_user(**roman)
    db.sudscribe_on_author(author_username="kpomak", **roman)
