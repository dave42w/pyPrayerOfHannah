import os
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from sqlmodel._compat import SQLModelConfig
from sqlalchemy import Column, String, Index, engine
from pydantic import computed_field
from enum import StrEnum
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool

class VerseType(StrEnum):
    VERSE = 'v'
    CHORUS = 'c'
    BRIDGE = 'b'

class DB:
    DATABASE_FILE = 'PrayerOfHannah.sqlite'
    DATABASE_URL = 'sqlite:///' + DATABASE_FILE

    # controls if the sql is logged
    ECHO_SQL = False

    def __init__(self) -> None:
        print("Creating DB Engine")
        self.engine: engine.Engine = create_engine(self.DATABASE_URL, echo=self.ECHO_SQL)
        print("Database Engine Connected")

    def create_database_structure(self) -> None:
        print("Creating Database Structure")
        SQLModel.metadata.create_all(self.engine)

    def delete_database(self) -> None:
        print("Delete database to start fresh")
        os.remove(self.DATABASE_FILE)

    #Maybe clean up with a dependency like:
    def get_session(self):
        with Session(self.engine) as session:
            yield session

class SQLModelValidation(SQLModel):
    """
    Helper class to allow for validation in SQLModel classes with table=True
    """

    model_config = SQLModelConfig(
        from_attributes=True, validate_assignment=True 
    )


def my_on_connect(dbapi_con, connection_record):
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


listen(Pool, "connect", my_on_connect)


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
    ----     ----   ---------   ----
       |     |              |      |
  -------------------   ------------------
  |Author_Song      |   |Song_Book_Item  |
  |M:M no extra data|   |M:M inc Song_Nbr|
  -------------------   | & verse_order  |
                        ------------------
                          ^         ^
                         1:M       1:M
                          |         |
                       -------   -------
                       |Verse|   |Media|
                       -------   -------

A song can have zero, one or many authors, the link is just the relationship

A song can be in zero, one or many Song_Books (held in Song_Book_Item). 
Each Song_Book_Item has a number within that Song_Book and a order for the verses

A Song_Book_Item can have zero, one or many Verses. Each Verse has an enumerated type 
(V-Verse, C-Chorus, B-Bridge) and a Markdown lyric

A Song_Book_Item can have zero, one or many media files. These have an 
enumerated type to control what is displayed
(BI=Background image, V=Video without lyrics, VL=Video with Lyrics, A=Audio only, AS=Audio with Singing, BV=Background video)
They also have a tune name and a verse count

'''


class Author_Song(SQLModelValidation, table=True):
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
    songs: list["Song"] = Relationship(back_populates="authors", link_model=Author_Song)

    __table_args__ = (
        Index(
            "compound_index_author_surname_firstnames",
            "surname",
            "firstnames",
            unique=True,
        ),
    )

    @computed_field # type: ignore[prop-decorator]
    @property
    def display_name(self) -> str:
        return (f"{self.surname}, {self.firstnames}")


class Song_Book(SQLModel, table=True):
    """
    A class to represent a published collection of Songs/Hymns


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    code :  str
        Short form of Book identifier eg StF
    name : str
        Name of the Song Book
    url : str
        Book website
    songs : list[Song_Book_Item]
        All the songs in this book

    """    
    id: int | None = Field(default=None, primary_key=True)

    code: str = Field(
        description="Short form of Book identifier eg StF",
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
        description="Book website",
        sa_column=Column("url", String(200), nullable=True),
        min_length=3, 
        max_length=200,
    )

    # M:M relationship with Song via link with extra data
    songs: list["Song_Book_Item"] = Relationship(back_populates="song_book")


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
    song_book_items : list[song_book_item]
        All the songs in this book
    """    
    id: int | None = Field(default=None, primary_key=True) 

    title: str = Field(
        description="Song title eg Be Thou My Vision",
        sa_column=Column("title", String(50), index=True, unique=True, nullable=False),
        min_length=5, 
        max_length=50,
    )

    # M:M relationship with Author via keys only link
    authors: list["Author"] = Relationship(back_populates="songs", link_model=Author_Song)

    # M:M relationship with Song_Book via link with extra data
    song_book_items: list["Song_Book_Item"] = Relationship(back_populates="song")


class Song_Book_Item(SQLModelValidation, table=True):
    """
    A class to represent the many to many link betweem song_book and song


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    song_book_id : int
        foreign key to song_book, part of unique index
    song_id : int
        foreign key to song, part of unique index
    nbr : int
        the Song Nbr in this book
    verse_order : str
        the order verses are displayed (eg V1 C1 V2 B1 C1 V3 C1)
    """    
    id: int | None = Field(default=None, primary_key=True) 
    song_book_id: int = Field(foreign_key="song_book.id")
    song_id: int = Field(foreign_key="song.id")
    nbr: int = Field(description="the Song Nbr in this book", nullable=False, ge=1, le=9999)
    verse_order: str = Field(
        description="List of the verses showing the order eg v1 b1 c1 v2 c1 v3 b1 c1",
        sa_column=Column("verse_order", String(20), nullable=True),
        min_length=0, 
        max_length=20,
    )

    song_book: "Song_Book" = Relationship(back_populates="songs")
    song: "Song" = Relationship(back_populates="song_book_items")

    verses: list["Verse"] = Relationship(back_populates="song_book_item")

    __table_args__ = (
        Index(
            "compound_index_song_book_item_fks",
            "song_book_id",
            "song_id",
            unique=True,
        ),
    )

class Verse(SQLModelValidation, table=True):
    """
    A class to represent a Verse of a song lyrics


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    song_book_item_id : int
        part of the Primary Key, foreign key to song_book
    type : str
        the verse type (see enum class VerseType)
    number : int
        the verse nbr
    lyrics : str
        markdown lyrics for this verse
    song_book_item : int
        foreign _key to song_book_item
    """    
    id: int | None = Field(default=None, primary_key=True) 
    type: VerseType = Field(description="the verse type", nullable=False)
    number: int = Field(description="the verse nbr", nullable=False, ge=1, le=10)
    lyrics: str = Field(
        description="markdown lyrics for this verse",
        sa_column=Column("lyrics", String(1000), nullable=True),
        min_length=0, 
        max_length=1000,
    )

    song_book_item_id: int = Field(foreign_key="song_book_item.id")

    song_book_item: "Song_Book_Item" = Relationship(back_populates="verses")

    __table_args__ = (
        Index(
            "compound_index_verse",
            "song_book_item_id",
            "type",
            "number",
            unique=True,
        ),
    )



def main() -> None:
    # Create a DB Instance
    db = DB()

    db.delete_database()
    db.create_database_structure()
    db.get_session()

    # Adding sample data
    with Session(db.engine) as session:

        a_wesley_john: Author = Author(surname="Wesley", firstnames="John")
        a_wesley_charles: Author = Author(surname="Wesley", firstnames="Charles")

        sb_HP: Song_Book = Song_Book(code="H&P", name="Hymns and Psalms")
        sb_StF: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")

        s_and: Song = Song(title="And Can it be",  authors=[a_wesley_charles])
        s_oh: Song = Song(title="Oh thou who camest from above", authors=[a_wesley_charles, a_wesley_john])

        sbi1: Song_Book_Item = Song_Book_Item(song_book=sb_StF, song=s_and, nbr=435, verse_order="v1 b1 c1 v2")
        sbi2: Song_Book_Item = Song_Book_Item(song_book=sb_HP, song=s_and, nbr=3)
        sbi3: Song_Book_Item = Song_Book_Item(song_book=sb_StF, song=s_oh, nbr=1, verse_order="v1 v2 v3")

        v1: Verse = Verse(type=VerseType.VERSE, number=1, lyrics="My first verse", song_book_item=sbi1)
        v2: Verse = Verse(type=VerseType.VERSE, number=2, lyrics="My second verse", song_book_item=sbi1)
        v3: Verse = Verse(type=VerseType.BRIDGE, number=1, lyrics="a bridge", song_book_item=sbi2)
        v4: Verse = Verse(type=VerseType.CHORUS, number=1, lyrics="a chorus", song_book_item=sbi3)
        
        session.add(a_wesley_john)
        session.add(a_wesley_charles)

        session.add(sb_HP)
        session.add(sb_StF)

        session.add(s_and)
        session.add(s_oh)

        session.add(sbi1)
        session.add(sbi2)
        session.add(sbi3)

        session.add(v1)
        session.add(v2)
        session.add(v3)
        session.add(v4)

        session.commit()

        print(f"John W id:{a_wesley_john.id}")
        print(f"Charles W id:{a_wesley_charles.id}")
        print(f"H&P id:{sb_HP.id}")
        print(f"StF id:{sb_StF.id}")
        print(f"And Can it Be id:{s_and.id}")
        print(f"Oh thou who camest from above id:{s_oh.id}")
        print("")
    
    print("Check many to many song to author")
    with Session(db.engine) as session:
        for s in session.exec(select(Song)).all():
            print(f"Song Title:{s.title} Authors:", end='')
            for auths in s.authors:
                print(f"{auths.display_name}; ", end='')
            print("")
        print("")

    print("Check many to many author to song")
    with Session(db.engine) as session:
        for auth in session.exec(select(Author)).all():
            print(f"Author: {auth.display_name} Songs: ", end='')
            for sngs in auth.songs:
                print(f"{sngs.title}; ", end='')
            print("")
        print("")


    print("Check many to many song to song book")
    with Session(db.engine) as session:
        for s2 in session.exec(select(Song)).all():
            print(f"Song Title:{s.title} Song Books:", end='')
            for b in s2.song_book_items:
                print(f"{b.song_book.code}:{b.song_book.name}:{b.song_book.url}:{b.nbr}:{b.verse_order}; ")
                for v in b.verses:
                    print(f"{v.type}:{v.number}:{v.lyrics}")
            print("")
        print("")

    print("Check many to many song book to song")
    with Session(db.engine) as session:
        for sb2 in session.exec(select(Song_Book)).all():
            print(f"Song Book:{sb2.code}:{sb2.name} Songs:", end='')
            for sn2 in sb2.songs:
                print(f"{sn2.nbr}:{sn2.song.title}:{sn2.verse_order}; ", end='')
            print("")
        print("")



if __name__ == "__main__":
    main()
