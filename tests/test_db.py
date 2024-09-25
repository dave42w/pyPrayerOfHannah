from pyPrayerOfHannah.dbms import Dbms, Author, Song_Book
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select, Sequence
from sqlmodel._compat import SQLModelConfig
from sqlalchemy import Column, String, Index, engine
import pytest
import pathlib as pl

@pytest.fixture  
def db() -> Dbms:  
    dbase = Dbms(True)
    dbase.delete_database()
    dbase.create_database_structure()
    return dbase

def test_delete_database_test() -> None:
    db = Dbms()
    db.delete_database()
    p: pl.Path = pl.Path(db.DATABASE_FILE)
    if p.resolve().is_file():
        raise AssertionError(f"Database File hasn't been deleted: {str(p)}")

def test_author(db: Dbms) -> None:
    with Session(db.engine) as session:

        row1: Author = Author(surname="Wesley", first_names="John")
        row1_check: Author = Author(surname="Wesley", first_names="John")
        row2: Author = Author(surname="Dobson", first_names="Marjorie")
        row2_check: Author = Author(surname="Dobson", first_names="Marjorie")
        
        session.add(row1)
        session.add(row2)

        session.commit()

        assert row1.id is not None, "Row should exist after add"
        assert row1.id == 1, f"Add id should be 1: {row1.id}"

        assert row1.surname == row1_check.surname, f"Author.surname should be '{row1_check.surname}' is '{row1.surname}'"
        assert row1.first_names == row1_check.first_names, f"Author.first_names should be '{row1_check.first_names}' is '{row1.first_names}'"
        assert row1.display_name == row1_check.display_name, f"Author.displayname should be '{row1_check.display_name}' is '{row1.surname}'"

        assert row2.id is not None, "Row should exist after add"
        assert row2.id == 2, f"Add id should be 2: {row2.id}"

        assert row2.surname == row2_check.surname, f"Author.surname should be '{row2_check.surname}' is '{row2.surname}'"
        assert row2.first_names == row2_check.first_names, f"Author.first_names should be '{row2_check.first_names}' is '{row2.first_names}'"
        assert row2.display_name == row2_check.display_name, f"Author.displayname should be '{row2_check.display_name}' is '{row2.surname}'"

    with Session(db.engine) as session:
        results = session.exec(select(Author).order_by(Author.surname, Author.first_names)).all()
        assert len(results) == 2, f"Should be 2 Rows is {len(results)}"
        r0: Author = results[0]
        r1: Author = results[1]
        assert r0.surname == row2_check.surname, f"First Author.surname should be '{row2_check.surname}' is '{r0.surname}'"
        assert r1.surname == row1_check.surname, f"First Author.surname should be '{row1_check.surname}' is '{r1.surname}'"

    with Session(db.engine) as session:
        a1: Author | None = session.get(Author, 1)
        assert a1 is not None, "Get id 1 failed"
        if isinstance(a1, Author):
            a1.surname = "Not Wesley"
            session.add(a1)
            session.commit()

    with Session(db.engine) as session:
        a2: Author | None = session.get(Author, 1)
        assert a2 is not None, "2nd Get id 1 should not have failed after update"
        if isinstance(a2, Author):
            assert a2.surname == "Not Wesley", f"Updated Author.surname should be 'Not Wesley' is '{a2.surname}'"
            session.delete(a2)
            session.commit()

    with Session(db.engine) as session:
        a3: Author | None = session.get(Author, 1)
        assert a3 is None, "Updated Author.surname should have been deleted"

        

def test_add_song_book(db) -> None:
    with Session(db.engine) as session:

        row: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")
        session.add(row)

        session.commit()

        assert row.id is not None, "Row should exist after add"
        assert row.id == 1, f"Add id should be 1: {row.id}"
        assert row.code == "StF", f"Add code should be 'StF': {row.code}"
        assert row.name == "Singing the Faith", "Add name should be 'Singing the Faith': {row.name}"
        assert row.url == "methodist.org", f"Add url should be 'methodist.org': {row.url}"
