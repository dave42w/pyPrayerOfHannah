from typing import cast
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import IntegrityError
import pytest

from dbs.models import Base
from dbs.models import Author

@pytest.fixture
def dbe():
    def _dbe() -> Engine:
        e: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
        Base.metadata.create_all(e)
        return e
    return _dbe


def test_add_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        surname: str ="AddWarnock"
        first_names: str = "AddDave Z"
        display_name: str = f"{surname}, {first_names}"
        expected_len: int = 1

        a1: Author = Author(surname=surname, first_names=first_names)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Author] = session.scalars(select(Author))
        l1 = len(s1.all())
        assert l1 == expected_len, f"Count is {l1} should be {expected_len}"

        s2: ScalarResult[Author] = session.scalars(select(Author))
        r2: Author = cast(Author, s2.first())
        assert r2.surname == surname, "Add author Surname is {r2.surname} should be {surname}"
        assert r2.first_names == first_names, "Add author first_names is {r2.first_names} should be {first_names}"
        assert r2.display_name == display_name, "Add author display_name is {r2.display_name} should be {display_name}"


def test_delete_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        surname: str ="DelWarnock"
        first_names: str = "DelDave Z"
        expected_len1: int = 1
        expected_len3: int = 0

        a1: Author = Author(surname=surname, first_names=first_names)
        session.add(a1)
        session.commit()

        s1: ScalarResult[Author] = session.scalars(select(Author))
        l1 = len(s1.all())
        assert l1 == expected_len1, f"Count is {l1} should be {expected_len1}"

        s2: ScalarResult[Author] = session.scalars(select(Author))
        r2: Author = cast(Author, s2.first())
        session.delete(r2)
        session.commit()

        s3: ScalarResult[Author] = session.scalars(select(Author))
        l3 = len(s3.all())
        assert l3 == expected_len3, f"Count is {l3} should be {expected_len3}"


def test_update_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        surname: str ="UpdWarnock"
        first_names: str = "UpdDave Z"
        surname_upd: str ="NotUpdWarnock"
        first_names_upd: str = "NotUpdDave Z"
        display_name_upd: str = f"{surname_upd}, {first_names_upd}"
        expected_len: int = 1

        a1: Author = Author(surname=surname, first_names=first_names)
        session.add(a1)
        session.commit()

        s2: ScalarResult[Author] = session.scalars(select(Author))
        r2: Author = cast(Author, s2.first())
        r2.surname=surname_upd
        r2.first_names=first_names_upd
        session.commit()

        s3: ScalarResult[Author] = session.scalars(select(Author))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Author] = session.scalars(select(Author))
        r4 = cast(Author, s4.first())
        assert r4.surname == surname_upd, "Update Author Surname is {r.surname} should be {surname_upd}"
        assert r4.first_names == first_names_upd, "Update Author first_names is {r.first_names} should be {first_names_upd}"
        assert r4.display_name == display_name_upd, "Update Author display_name is {r.display_name} should be {display_name_upd}"


def test_no_duplicate_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        surname: str ="DupWarnock"
        first_names: str = "DupDave Z"
        display_name: str = f"{surname}, {first_names}"
        expected_len: int = 1

        a1: Author = Author(surname=surname, first_names=first_names)
        session.add(a1)
        session.commit()

        a2: Author = Author(surname=surname, first_names=first_names)
        session.add(a2)
        with pytest.raises(IntegrityError):
            session.commit()

    with Session(e) as session:
        s3: ScalarResult[Author] = session.scalars(select(Author))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Count is {l3} should be {expected_len}"

        s4: ScalarResult[Author] = session.scalars(select(Author))
        r4: Author = cast(Author, s4.first())
        assert r4.surname == surname, "Dup author Surname is {r4.surname} should be {surname}"
        assert r4.first_names == first_names, "Dup author first_names is {r4.first_names} should be {first_names}"
        assert r4.display_name == display_name, "Dup author display_name is {r4.display_name} should be {display_name}"
