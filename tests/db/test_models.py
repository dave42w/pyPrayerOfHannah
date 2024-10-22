from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import pytest

from dbs.models import Base
from dbs.models import Author

@pytest.fixture
def dbe():
    def _dbe() -> Engine:
        # Connect to the specified database
        e: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        Base.metadata.create_all(e)
        return e
    return _dbe

def test_add_author(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        a: Author = Author(surname="Warnock", first_names="Dave Z")     # type: ignore[call-arg]
        session.add(a)
        session.commit
