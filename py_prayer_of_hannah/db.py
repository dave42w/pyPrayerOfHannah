import os
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from sqlmodel._compat import SQLModelConfig
from sqlalchemy import Column, String, event
#from pydantic import EmailStr

ECHO_SQL = True

# Create an ENGINE (connection to the database)
ENGINE = create_engine('sqlite:///PrayerOfHannah.sqlite', echo=ECHO_SQL)
print("Database Engine Connected")

class SQLModelValidation(SQLModel):
    """
    Helper class to allow for validation in SQLModel classes with table=True
    """

    model_config = SQLModelConfig(
        from_attributes=True, validate_assignment=True 
    )

ECHO_SQL = True
# Create an ENGINE (connection to the database)
ENGINE = create_engine('sqlite:///PrayerOfHannah.sqlite', echo=ECHO_SQL)
print("Database Engine Connected")

@event.listens_for(ENGINE, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#Maybe clean up with a dependency like:
def get_session():
    with Session(ENGINE) as session:
        yield session

class Author(SQLModelValidation, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Primary Key

    name: str = Field(
        description="Author name eg 'Wesley, John'",
        sa_column=Column("name", String(50), unique=True, index=True, nullable=False),
        min_length=3, 
        max_length=50,
    )

    songs: list["Song"] = Relationship(back_populates="author")

class Song_Collection(SQLModelValidation, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Primary Key

    code: str = Field(
        description="Short code identifying the collection of songs eg StF for Singing the Faith",
        sa_column=Column("code", String(10), unique=True, index=True, nullable=False),
        min_length=2, 
        max_length=10,
    )

    url: str = Field(
        description="Collection website",
        sa_column=Column("url", String(200), nullable=True),
        min_length=3, 
        max_length=200,
    )

    songs: list["Song"] = Relationship(back_populates="song_collection")

class Song(SQLModelValidation, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Primary Key

    title: str = Field(
        description="Primary song title",
        sa_column=Column("code", String(200), unique=True, index=True, nullable=False),
        min_length=2, 
        max_length=200,
    )

    author_id: int = Field(foreign_key="author.id", ondelete="RESTRICT")
    song_collection_id: int = Field(foreign_key="song_collection.id", ondelete="RESTRICT")

    author: Author = Relationship(back_populates="songs")
    song_collection: Song_Collection = Relationship(back_populates="songs")


SQLModel.metadata.create_all(ENGINE)
print("Database Created")

def main():
    print("Delete database")
    os.remove("PrayerOfHannah.sqlite")

    print("Create Database")
    SQLModel.metadata.create_all(ENGINE)

if __name__ == "__main__":
    main()
