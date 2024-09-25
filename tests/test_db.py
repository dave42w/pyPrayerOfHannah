from pyPrayerOfHannah.db import DB, Author
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
    d.create_database_structure()
    d.get_session()

    with Session(d.engine) as session:

        a_wesley_john: Author = Author(surname="Wesley", firstnames="John")
        session.add(a_wesley_john)

        session.commit()

        if a_wesley_john.id != 1: 
            raise AssertionError(f"Add author id should be 1: {a_wesley_john.id}")

        if a_wesley_john.surname != "Wesley": 
            raise AssertionError(f"Add author surname should be 'Wesley': {a_wesley_john.surname}")

        if a_wesley_john.firstnames != "John": 
            raise AssertionError(f"Add author firstnames should be 'John': {a_wesley_john.firstnames}")

        if a_wesley_john.display_name != "Wesley, John": 
            raise AssertionError(f"Add author displayname should be 'Wesley, John': {a_wesley_john.display_name}")
