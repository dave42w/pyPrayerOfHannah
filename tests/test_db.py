from pyPrayerOfHannah.dbms import Dbms, Author, Song_Book
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from sqlmodel._compat import SQLModelConfig
from sqlalchemy import Column, String, Index, engine

import pathlib as pl

def test_delete_database_test() -> None:
    db = Dbms()
    db.delete_database()
    p: pl.Path = pl.Path(db.DATABASE_FILE)
    if p.resolve().is_file():
        raise AssertionError(f"Database File hasn't been deleted: {str(p)}")

def test_add_author() -> None:
    db = Dbms(True)
    db.delete_database()
    db.create_database_structure()
    db.get_session()

    with Session(db.engine) as session:

        row: Author = Author(surname="Wesley", firstnames="John")
        session.add(row)

        session.commit()

        assert row.id is not None, "Row should exist after add"
        assert row.id == 1, f"Add id should be 1: {row.id}"

        assert row.surname == "Wesley", f"Add author surname should be 'Wesley': {row.surname}"
        assert row.firstnames == "John", f"Add author firstnames should be 'John': {row.firstnames}"
        assert row.display_name == "Wesley, John", f"Add author displayname should be 'Wesley, John': {row.display_name}"

def test_add_song_book() -> None:
    db = Dbms(True)

    db.delete_database()
    db.create_database_structure()
    db.get_session()

    with Session(db.engine) as session:

        row: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")
        session.add(row)

        session.commit()

        assert row.id is not None, "Row should exist after add"
        assert row.id == 1, f"Add id should be 1: {row.id}"
        assert row.code == "StF", f"Add code should be 'StF': {row.code}"
        assert row.name == "Singing the Faith", "Add name should be 'Singing the Faith': {row.name}"
        assert row.url == "methodist.org", f"Add url should be 'methodist.org': {row.url}"
