import os
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from sqlmodel._compat import SQLModelConfig
from sqlalchemy import event, Column, String, Index
from pydantic import computed_field

# controls if the sql is logged
ECHO_SQL = False

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


@event.listens_for(ENGINE, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#Maybe clean up with a dependency like:
def get_session():
    with Session(ENGINE) as session:
        yield session


'''
Db structure

----------                 -----------
| Author |                 |Song_Book| 
----------                 -----------
    ^                           ^ 
   1:M        --------         1:M
    |         | Song |          | 
    |         --------          |
    |           ^   ^           |
    |          1:M 1:M          |
    |           |   |           |
    ----     ----   ------      |
       |     |           |      |
  ------------------   ----------------
  |Song_Author_Link|   |Song_Book_Item|
  ------------------   ----------------
   M:M no extra data    M:M inc Song_Nbr


A song can have zero, one or many authors, the link is just the relationship

A song can be in zero, one or many Song_Books and each time it has a number within that Song_Book

'''


class Author_Song_Link(SQLModelValidation, table=True):
    """
    A class to represent the many to many link betweem author and song


    Attributes
    ----------
    author_id : int
        part of the Primary Key, foreign key to author
    song_id : int
        part of the Primary Key, foreign key to song

    """    
    author_id: int = Field(foreign_key="author.id", primary_key=True)
    song_id: int = Field(foreign_key="song.id", primary_key=True)


class Author(SQLModelValidation, table=True):
    """
    A class to represent the Song/Tune writers.


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    surname : str
        Surname of the Author
    firstnames : str
        All First names and initials of the Author
    songs : list[songs]
        All the songs by this author

    """    
    id: int | None = Field(default=None, primary_key=True) 

    surname: str = Field(
        description="Author surname eg 'Wesley'",
        sa_column=Column("surname", String(50), nullable=False),
        min_length=3, 
        max_length=50,
    )

    firstnames: str = Field(
        description="Author firstnames eg 'John Fred' or 'John F'",
        sa_column=Column("firstnames", String(50), nullable=False),
        min_length=0, 
        max_length=50,
    )

    # M:M relationship with Song via keys only link
    songs: list["Song"] = Relationship(back_populates="authors", link_model=Author_Song_Link)

    __table_args__ = (
        Index(
            "compound_index_author_surname_firstnames",
            "surname",
            "firstnames",
        ),
    )

    @computed_field
    @property
    def display_name(self) -> str:
        return (f"{self.surname}, {self.firstnames}")

class Song_Book_Song_Link(SQLModelValidation, table=True):
    """
    A class to represent the many to many link betweem song_book and song


    Attributes
    ----------
    song_book_id : int
        part of the Primary Key, foreign key to song_book
    song_id : int
        part of the Primary Key, foreign key to song
    nbr : int
        the Song Nbr in this book
    """    
    song_book_id: int = Field(foreign_key="song_book.id", primary_key=True)
    song_id: int = Field(foreign_key="song.id", primary_key=True)
    nbr: int = Field(description="the Song Nbr in this book", nullable=False, ge=1, le=9999)

    song_book: "Song_Book" = Relationship(back_populates="song_links")
    song: "Song" = Relationship(back_populates="song_book_links")


class Song_Book(SQLModel, table=True):
    """
    A class to represent a published collection of Songs/Hymns


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    name : str
        Name of the Song Book
    songs : list[songs]
        All the songs in this book

    """    
    id: int | None = Field(default=None, primary_key=True)

    code: str = Field(
        description="Short form of Book identifier eg StF Faith",
        sa_column=Column("code", String(10), index=True, unique=True, nullable=False),
        min_length=1, 
        max_length=10,
    )

    name: str = Field(
        description="Book name eg Singing the Faith",
        sa_column=Column("name", String(50), index=True, unique=True, nullable=False),
        min_length=5, 
        max_length=50,
    )

    url: str = Field(
        description="Collection website",
        sa_column=Column("url", String(200), nullable=True),
        min_length=3, 
        max_length=200,
    )

    # M:M relationship with Song via link with extra data
    song_links: list[Song_Book_Song_Link] = Relationship(back_populates="song_book")


class Song(SQLModelValidation, table=True):
    """
    A class to represent a published song 


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    title : str
        Name of the Song
    authors : list[authors]
        All the authors of this book
    song_books : list[song_books]
        All the authors of this book
    """    
    id: int | None = Field(default=None, primary_key=True)  # Primary Key

    title: str = Field(
        description="Song title eg Be Thou My Vision",
        sa_column=Column("title", String(50), index=True, unique=True, nullable=False),
        min_length=5, 
        max_length=50,
    )

    # M:M relationship with Author via keys only link
    authors: list["Author"] = Relationship(back_populates="songs", link_model=Author_Song_Link)

    # M:M relationship with Song_Book via link with extra data
    song_book_links: list[Song_Book_Song_Link] = Relationship(back_populates="song")



def main() -> None:

    print("Delete database to start fresh")
    os.remove("PrayerOfHannah.sqlite")

    print("Create Database Structure")
    SQLModel.metadata.create_all(ENGINE)

    # Adding sample data
    with Session(ENGINE) as session:

        a_wesley_john: Author = Author(surname="Wesley", firstnames="John")
        a_wesley_charles: Author = Author(surname="Wesley", firstnames="Charles")

        sb_HP: Song_Book = Song_Book(code="H&P", name="Hymns and Psalms")
        sb_StF: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")

        s_and: Song = Song(title="And Can it be",  authors=[a_wesley_charles])
        s_oh: Song = Song(title="Oh thou who camest from above", authors=[a_wesley_charles, a_wesley_john])

        sbl1: Song_Book_Song_Link = Song_Book_Song_Link(song_book=sb_StF, song=s_and, nbr=435)
        sbl2: Song_Book_Song_Link = Song_Book_Song_Link(song_book=sb_HP, song=s_and, nbr=3)
        sbl3: Song_Book_Song_Link = Song_Book_Song_Link(song_book=sb_StF, song=s_oh, nbr=1)
        
        session.add(a_wesley_john)
        session.add(a_wesley_charles)

        session.add(sb_HP)
        session.add(sb_StF)

        session.add(s_and)
        session.add(s_oh)

        session.add(sbl1)
        session.add(sbl2)
        session.add(sbl3)

        session.commit()

        print(f"John W id:{a_wesley_john.id}")
        print(f"Charles W id:{a_wesley_charles.id}")
        print(f"H&P id:{sb_HP.id}")
        print(f"StF id:{sb_StF.id}")
        print(f"And Can it Be id:{s_and.id}")
        print(f"Oh thou who camest from above id:{s_oh.id}")
        print("")
    
    print("Check many to many song to author")
    with Session(ENGINE) as session:
        for s in session.exec(select(Song)).all():
            print(f"Song Title:{s.title} Authors:", end='')
            for auths in s.authors:
                print(f"{auths.display_name}; ", end='')
            print("")
        print("")

    print("Check many to many author to song")
    with Session(ENGINE) as session:
        for auth in session.exec(select(Author)).all():
            print(f"Author: {auth.display_name} Songs: ", end='')
            for sngs in auth.songs:
                print(f"{sngs.title}; ", end='')
            print("")
        print("")


    print("Check many to many song to song book")
    with Session(ENGINE) as session:
        for s2 in session.exec(select(Song)).all():
            print(f"Song Title:{s.title} Song Books:", end='')
            for b in s2.song_book_links:
                print(f"{b.song_book.code}:{b.song_book.name}:{b.song_book.url}:{b.nbr}; ", end='')
            print("")
        print("")

    print("Check many to many song book to song")
    with Session(ENGINE) as session:
        for sb2 in session.exec(select(Song_Book)).all():
            print(f"Song Book:{sb2.code}:{sb2.name} Songs:", end='')
            for sn2 in sb2.song_links:
                print(f"{sn2.nbr}:{sn2.song.title}; ", end='')
            print("")
        print("")



if __name__ == "__main__":
    main()


'''

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
'''