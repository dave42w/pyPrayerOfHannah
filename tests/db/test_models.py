from typing import cast
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
import pytest

from dbs.models import Base
from dbs.models import Author, Song_Book

@pytest.fixture
def dbe():
    def _dbe() -> Engine:
        e: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
        Base.metadata.create_all(e)
        return e
    return _dbe

def get_test_author(session: Session) -> ScalarResult[Author]:
    return session.scalars(select(Author))

def get_test_song_book(session: Session) -> ScalarResult[Author]:
    return session.scalars(select(Song_Book))


def test_add_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        a: Author = Author(surname="Warnock", first_names="Dave Z")
        session.add(a)
        session.commit()

    with Session(e) as session:
        a1: ScalarResult[Author] = get_test_author(session)
        c: int = len(a1.all())
        assert c == 1, f"{c}: should be one author in table"

    with Session(e) as session:
        a2: ScalarResult[Author] = get_test_author(session)
        ar: Author = cast(Author, a2.first())
        assert ar.surname == "Warnock", "Surname should be warnock"
        assert ar.first_names == "Dave Z", "First names should be Dave Z"


def test_add_song_book(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        s: Song_Book = Song_Book(code="StF", name="Singing the Faith", url=None)
        session.add(s)
        session.commit()

    with Session(e) as session:
        s1: ScalarResult[Song_Book] = get_test_song_book(session)
        c: int = len(s1.all())
        assert c == 1, f"{c}: should be one song_book in table"

    with Session(e) as session:
        s2: ScalarResult[Author] = get_test_song_book(session)
        sr: Song_Book = cast(Song_Book, s2.first())
        assert sr.code == "StF", f"{sr.code}: Code should be StF"
        assert sr.name == "Singing the Faith", f"{sr.name}: Name should be Singing the Faith"
