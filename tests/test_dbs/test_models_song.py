from typing import cast
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import IntegrityError
import pytest

from dbs.models import Base
from dbs.models import Song

@pytest.fixture
def dbe():
    def _dbe() -> Engine:
        e: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
        Base.metadata.create_all(e)
        return e
    return _dbe


def test_add_song(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        title: str ="AddAnd Can It Be"
        expected_len: int = 1

        a1: Song = Song(title=title)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Song] = session.scalars(select(Song))
        l1 = len(s1.all())
        assert l1 == expected_len, f"Count is {l1} should be {expected_len}"

        s2: ScalarResult[Song] = session.scalars(select(Song))
        r2: Song = cast(Song, s2.first())
        assert r2.title == title, "Add song title is {r2.title} should be {title}"


def test_delete_song(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        title: str ="DelAnd Can It Be"
        expected_len1: int = 1
        expected_len3: int = 0

        a1: Song = Song(title=title)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Song] = session.scalars(select(Song))
        l1 = len(s1.all())
        assert l1 == expected_len1, f"Count is {l1} should be {expected_len1}"

        s2: ScalarResult[Song] = session.scalars(select(Song))
        r2: Song = cast(Song, s2.first())
        session.delete(r2)
        session.commit()

        s3: ScalarResult[Song] = session.scalars(select(Song))
        l3 = len(s3.all())
        assert l3 == expected_len3, f"Count is {l3} should be {expected_len3}"


def test_update_song(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        title: str ="UpdAnd Can It Be"
        title_upd: str ="NotUpdAnd Can It Be"
        expected_len: int = 1

        a1: Song = Song(title=title)
        session.add(a1)
        session.commit()

        s2: ScalarResult[Song] = session.scalars(select(Song))
        r2: Song = cast(Song, s2.first())
        r2.title=title_upd
        session.commit()

        s3: ScalarResult[Song] = session.scalars(select(Song))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Song] = session.scalars(select(Song))
        r4 = cast(Song, s4.first())
        assert r4.title == title_upd, "Update Song title is {r.title} should be {title_upd}"


def test_no_duplicate_song(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        title: str ="DupAnd Can It Be"
        first_names: str = "DupDave Z"
        display_name: str = f"{title}, {first_names}"
        expected_len: int = 1

        a1: Song = Song(title=title)
        session.add(a1)
        session.commit()

        a2: Song = Song(title=title)
        session.add(a2)
        with pytest.raises(IntegrityError):
            session.commit()

    with Session(e) as session:
        s3: ScalarResult[Song] = session.scalars(select(Song))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Song] = session.scalars(select(Song))
        r4: Song = cast(Song, s4.first())
        assert r4.title == title, "Dup song title is {r4.title} should be {title}"
