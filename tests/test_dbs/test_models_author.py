from typing import cast, Any
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

def add_test_row(session: Session) -> None:
    a: Author = Author(surname="Warnock", first_names="Dave Z")
    session.add(a)
    session.commit()


def get_test_rows(session: Session) -> ScalarResult[Author]:
    return session.scalars(select(Author))

def get_row_count(session: Session) -> int:
    o: ScalarResult[Any] = get_test_rows(session)
    return len(o.all())


def test_add_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:

        add_test_row(session)

        assert get_row_count(session) == 1, f"Add author {get_row_count(session)}: should be one author in table"

        o: ScalarResult[Author] = get_test_rows(session)
        r: Author = cast(Author, o.first())
        assert r.surname == "Warnock", "Add author Surname should be Warnock"
        assert r.first_names == "Dave Z", "Add author First names should be Dave Z"
        assert r.display_name == "Warnock, Dave Z", "Add author Display name should be Warnock, Dave Z"


def test_delete_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        add_test_row(session)

        o: ScalarResult[Author] = get_test_rows(session)
        r: Author = cast(Author, o.first())
        session.delete(r)
        session.commit()

        assert get_row_count(session) == 0, f"delete author {get_row_count(session)}: should be zero author in table"


def test_update_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        add_test_row(session)

        o: ScalarResult[Author] = get_test_rows(session)
        r: Author = cast(Author, o.first())
        r.surname="Not Warnock"
        session.commit()

        assert get_row_count(session) == 1, f"Update author {get_row_count(session)}: should be one author in table"

        o = get_test_rows(session)

        r = cast(Author, o.first())
        assert r.surname == "Not Warnock", "Update Author Surname should be Not Warnock"
        assert r.first_names == "Dave Z", "Update Author First names should be Dave Z"
        assert r.display_name == "Not Warnock, Dave Z", "Update author Display name should be Not Warnock, Dave Z"


def test_no_duplicate_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        add_test_row(session)

        r: Author = Author(surname="Warnock", first_names="Dave Z")
        session.add(r)
        with pytest.raises(IntegrityError):
            session.commit()

    with Session(e) as session:
        assert get_row_count(session) == 1, f"No Duplicate author {get_row_count(session)}: should be one author in table"

        o: ScalarResult[Author] = get_test_rows(session)
        r = cast(Author, o.first())
        assert r.surname == "Warnock", "No Duplicate author Surname should be warnock"
        assert r.first_names == "Dave Z", "No Duplicate author First names should be Dave Z"
