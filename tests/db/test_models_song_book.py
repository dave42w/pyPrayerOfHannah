from typing import cast, Any
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import IntegrityError
import pytest

from dbs.models import Base
from dbs.models import Song_Book

@pytest.fixture
def dbe():
    def _dbe() -> Engine:
        e: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
        Base.metadata.create_all(e)
        return e
    return _dbe

def add_test_row(e: Engine) -> None:
    with Session(e) as session:
        o: Song_Book = Song_Book(code="StF", name="Singing the Faith", url=None)
        session.add(o)
        session.commit()

def get_test_rows(session: Session) -> ScalarResult[Song_Book]:
    return session.scalars(select(Song_Book))


def get_row_count(e: Engine) -> int:
    with Session(e) as session:
        o: ScalarResult[Any] = get_test_rows(session)
        return len(o.all())


def test_add_song_book(dbe) -> None:
    e: Engine = dbe()
    add_test_row(e)

    assert get_row_count(e) == 1, f"Add song_book {get_row_count(e)}: should be one song_book in table"

    with Session(e) as session:
        o: ScalarResult[Song_Book] = get_test_rows(session)
        r: Song_Book = cast(Song_Book, o.first())
        assert r.code == "StF", f"Add Song_Book Code: {r.code} should be StF"
        assert r.name == "Singing the Faith", f"Add Song_Book name: {r.name} should be Singing the Faith"
        assert r.url is None, f"Add Song_Book url: {r.url} should be none"

def test_delete_song_book(dbe) -> None:
    e: Engine = dbe()
    add_test_row(e)

    with Session(e) as session:
        o: ScalarResult[Song_Book] = get_test_rows(session)
        r: Song_Book = cast(Song_Book, o.first())
        session.delete(r)
        session.commit()

    assert get_row_count(e) == 0, f"Delete song_book {get_row_count(e)}: should be zero song_book in table"

def test_update_song_book(dbe) -> None:
    e: Engine = dbe()
    add_test_row(e)

    with Session(e) as session:
        o: ScalarResult[Song_Book] = get_test_rows(session)
        r: Song_Book = cast(Song_Book, o.first())
        r.name="Not Singing The Faith"
        session.commit()

    assert get_row_count(e) == 1, f"Update song_book {get_row_count(e)}: should be one song_book in table"

    with Session(e) as session:
        o = get_test_rows(session)
        r = cast(Song_Book, o.first())
        assert r.code == "StF", f"Update song_book: {r.code} Code should be StF"
        assert r.name == "Not Singing The Faith", f"Update song_book: {r.name} Name should be Not Singing the Faith"


def test_no_duplicate_song_book_code(dbe) -> None:
    e: Engine = dbe()
    add_test_row(e)

    with Session(e) as session:
        r: Song_Book = Song_Book(code="StF", name="Not Singing the Faith", url=None)

        session.add(r)
        with pytest.raises(IntegrityError):
            session.commit()

    assert get_row_count(e) == 1, f"No Duplicate song_book code: {get_row_count(e)}: should be one song_book in table"

    with Session(e) as session:
        o: ScalarResult[Song_Book] = get_test_rows(session)
        r = cast(Song_Book, o.first())
        assert r.code == "StF", f"No Duplicate song_book Code {r.code}: Code should be StF"
        assert r.name == "Singing the Faith", f"No Duplicate song_book code {r.name}: Name should be Singing the Faith"

def test_no_duplicate_song_book_name(dbe) -> None:
    e: Engine = dbe()
    add_test_row(e)

    with Session(e) as session:
        r: Song_Book = Song_Book(code="Not StF", name="Singing the Faith", url=None)

        session.add(r)
        with pytest.raises(IntegrityError):
            session.commit()

    assert get_row_count(e) == 1, f"No Duplicate song_book name {get_row_count(e)}: should be one song_book in table"

    with Session(e) as session:
        o: ScalarResult[Song_Book] = get_test_rows(session)
        r = cast(Song_Book, o.first())
        assert r.code == "StF", f"No Duplicate song_book name {r.code}: Code should be StF"
        assert r.name == "Singing the Faith", f"No Duplicate song_book name {r.name}: Name should be Singing the Faith"