import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy import engine
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool
import pathlib as pl

class Dbms:
    DATABASE_FILE = 'PrayerOfHannah.sqlite'
    DATABASE_URL = 'sqlite:///' + DATABASE_FILE

    # controls if the sql is logged
    ECHO_SQL = False

    def __init__(self, in_memory: bool = False) -> None:
        self.in_memory = in_memory
        if self.in_memory:
            print("Creating memory DB Engine")
            self.engine: engine.Engine = create_engine("sqlite://", echo=self.ECHO_SQL)
            print("Database Memory Engine Connected")
        else:
            print("Creating file DB Engine")
            self.engine = create_engine(self.DATABASE_URL, echo=self.ECHO_SQL)
            print("Database Engine Connected")

    def create_database_structure(self) -> None:
        print("Creating Database Structure")
        SQLModel.metadata.create_all(self.engine)

    def delete_database_file(self) -> None:
        if self.in_memory:
            print("In memory DB Engine so not deleted")
        else:
            path: pl.Path = pl.Path(self.DATABASE_FILE)
            if pl.Path(path).resolve().is_file():
                print("Delete database to start fresh")
                os.remove(self.DATABASE_FILE)
            else:
                print("No database to delete")


def my_on_connect(dbapi_con, connection_record):
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


listen(Pool, "connect", my_on_connect)
