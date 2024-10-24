from typing import cast
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


def test_add_song_book(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        code: str ="AddStF"
        name: str = "AddSinging the Faith"
        url: str | None = None
        expected_len: int = 1

        a1: Song_Book = Song_Book(code=code, name=name, url=url)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l1 = len(s1.all())
        assert l1 == expected_len, f"Count is {l1} should be {expected_len}"

        s2: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r2: Song_Book = cast(Song_Book, s2.first())
        assert r2.code == code, "Add song_book Code is {r2.code} should be {code}"
        assert r2.name == name, "Add song_book name is {r2.name} should be {name}"
        assert r2.url is None, "Add song_book url is {r2.url} should be None"


def test_add_song_book_with_url(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        code: str ="AddUrlStF"
        name: str = "AddUrlSinging the Faith"
        url: str = "AddUrl"
        expected_len: int = 1

        a1: Song_Book = Song_Book(code=code, name=name, url=url)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l1 = len(s1.all())
        assert l1 == expected_len, f"Count is {l1} should be {expected_len}"

        s2: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r2: Song_Book = cast(Song_Book, s2.first())
        assert r2.code == code, "Add song_book Code is {r2.code} should be {code}"
        assert r2.name == name, "Add song_book name is {r2.name} should be {name}"
        assert r2.url == url, "Add song_book url is {r2.url} should be {url}"


def test_delete_song_book(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        code: str ="DelStF"
        name: str = "DelSinging the Faith"
        url: str | None = None
        expected_len1: int = 1
        expected_len3: int = 0

        a1: Song_Book = Song_Book(code=code, name=name, url=url)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l1 = len(s1.all())
        assert l1 == expected_len1, f"Count is {l1} should be {expected_len1}"

        s2: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r2: Song_Book = cast(Song_Book, s2.first())
        session.delete(r2)
        session.commit()

        s3: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l3 = len(s3.all())
        assert l3 == expected_len3, f"Count is {l3} should be {expected_len3}"


def test_update_song_book(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        code: str ="UpdStF"
        name: str = "UpdSinging the Faith"
        url: str | None = None
        code_upd: str ="NotUpdStF"
        name_upd: str = "NotUpdSinging the Faith"
        expected_len: int = 1

        a1: Song_Book = Song_Book(code=code, name=name, url=url)
        session.add(a1)
        session.commit()

        s2: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r2: Song_Book = cast(Song_Book, s2.first())
        r2.code=code_upd
        r2.name=name_upd
        session.commit()

        s3: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r4 = cast(Song_Book, s4.first())
        assert r4.code == code_upd, "Update Song_Book Code is {r.code} should be {code_upd}"
        assert r4.name == name_upd, "Update Song_Book name is {r.name} should be {name_upd}"


def test_no_duplicate_song_book_code(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        code: str ="DupStF"
        name: str = "DupSinging the Faith"
        name2: str = "DupSinging the Faith2"
        url: str | None = None
        expected_len: int = 1

        a1: Song_Book = Song_Book(code=code, name=name, url=url)
        session.add(a1)
        session.commit()

        a2: Song_Book = Song_Book(code=code, name=name2, url=url)
        session.add(a2)
        with pytest.raises(IntegrityError):
            session.commit()

    with Session(e) as session:
        s3: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r4: Song_Book = cast(Song_Book, s4.first())
        assert r4.code == code, "Dup song_book Code is {r4.code} should be {code}"
        assert r4.name == name, "Dup song_book name is {r4.name} should be {name}"


def test_no_duplicate_song_book_name(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        code: str ="DupStF"
        code2: str ="DupStF2"
        name: str = "DupSinging the Faith"
        url: str | None = None
        expected_len: int = 1

        a1: Song_Book = Song_Book(code=code, name=name, url=url)
        session.add(a1)
        session.commit()

        a2: Song_Book = Song_Book(code=code2, name=name, url=url)
        session.add(a2)
        with pytest.raises(IntegrityError):
            session.commit()

    with Session(e) as session:
        s3: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Song_Book] = session.scalars(select(Song_Book))
        r4: Song_Book = cast(Song_Book, s4.first())
        assert r4.code == code, "Dup song_book Code is {r4.code} should be {code}"
        assert r4.name == name, "Dup song_book name is {r4.name} should be {name}"
