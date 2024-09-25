from pyPrayerOfHannah.db import DB, Author, Song_Book
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from sqlmodel._compat import SQLModelConfig
from sqlalchemy import Column, String, Index, engine

import pathlib as pl

def test_delete_database_test() -> None:
    d = DB()
    d.delete_database()
    p: pl.Path = pl.Path(d.DATABASE_FILE)
    if p.resolve().is_file():
        raise AssertionError(f"Database File hasn't been deleted: {str(p)}")

def test_add_author() -> None:
    d = DB()
    d.delete_database()
    d.create_database_structure()
    d.get_session()

    with Session(d.engine) as session:

        row: Author = Author(surname="Wesley", firstnames="John")
        session.add(row)

        session.commit()

        if row.id != 1: 
            raise AssertionError(f"Add id should be 1: {row.id}")

        if row.surname != "Wesley": 
            raise AssertionError(f"Add author surname should be 'Wesley': {row.surname}")

        if row.firstnames != "John": 
            raise AssertionError(f"Add author firstnames should be 'John': {row.firstnames}")

        if row.display_name != "Wesley, John": 
            raise AssertionError(f"Add author displayname should be 'Wesley, John': {row.display_name}")

def test_add_song_book() -> None:
    d = DB()
    d.delete_database()
    d.create_database_structure()
    d.get_session()

    with Session(d.engine) as session:

        row: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")
        session.add(row)

        session.commit()

        if row.id != 1: 
            raise AssertionError(f"Add id should be 1: {row.id}")

        if row.code != "StF": 
            raise AssertionError(f"Add code should be 'StF': {row.code}")

        if row.name != "Singing the Faith": 
            raise AssertionError(f"Add name should be 'Singing the Faith': {row.name}")

        if row.url != "methodist.org": 
            raise AssertionError(f"Add url should be 'methodist.org': {row.url}")
