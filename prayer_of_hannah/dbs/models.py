from typing import Optional
from typing import List

from sqlalchemy import String

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.schema import ForeignKey

from sqlalchemy.ext.hybrid import hybrid_property

from enum import StrEnum

class VerseType(StrEnum):
    VERSE = 'v'
    CHORUS = 'c'
    BRIDGE = 'b'
    ENDING = 'e'


class Base(MappedAsDataclass, DeclarativeBase):
    pass

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

class Author(Base):
    """
    A class to represent the Song/Tune writers.


    Attributes
    ----------
    id : int
        Primary Key, autoincremented
    surname : str
        Surname of the Author
    first_names : str
        All First names and initials of the Author
    songs : list[songs]
        All the songs by this author

    """
    __tablename__: str = "author"

    __table_args__ = (UniqueConstraint("surname", "first_names", name="unique_author_surname_first_names"),)

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    surname: Mapped[str] = mapped_column(String(50))                        # type: ignore[misc]
    first_names: Mapped[str] = mapped_column(String(50))                    # type: ignore[misc]

    songs: Mapped[List["Author_Song"]] = relationship(back_populates="author")     # type: ignore[misc]

    @hybrid_property
    def display_name(self):
        return (f"{self.surname}, {self.first_names}")


class Song_Book(Base):
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
    __tablename__: str = "song_book"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    code: Mapped[str] = mapped_column(String(10), index=True, unique=True)              # type: ignore[misc]
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True)              # type: ignore[misc]
    url: Mapped[Optional[str]] = mapped_column(String(200), index=True, unique=True)    # type: ignore[misc]

    #songs: Mapped[List["Song_Book_Item"]] = relationship(back_populates="song_book")    # type: ignore[misc]


class Song(Base):
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
    __tablename__: str = "song"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String(100), index=True, unique=True)                # type: ignore[misc]

    authors: Mapped[List["Author_Song"]] = relationship(back_populates="song")              # type: ignore[misc]
    #song_book_items: Mapped[List["Song_Book_Item"]] = relationship(back_populates="song")   # type: ignore[misc]



class Author_Song(Base):
    """
    A class to represent the many to many link between author and song


    Attributes
    ----------
    author_id : int
        part of the Primary Key, foreign key to author
    song_id : int
        part of the Primary Key, foreign key to song

    """
    __tablename__: str = "author_song"
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), primary_key=True, init=False)
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"), primary_key=True, init=False)

    author: Mapped["Author"] = relationship(back_populates="songs")     # type: ignore[misc]
    song: Mapped["Song"] = relationship(back_populates="authors")       # type: ignore[misc]


class Song_Book_Item(Base):
    """
    A class to represent the many to many link between song_book and song


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
    __tablename__: str = "song_book_item"

    __table_args__ = (
        UniqueConstraint("song_book_id", "song_id", name="unique_song_book_id_song_id"),
        )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    song_book_id: Mapped[int] = mapped_column(ForeignKey("song_book.id"))               # type: ignore[misc]
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"))                         # type: ignore[misc]

    nbr: Mapped[int]                                                                    # type: ignore[misc]
    verse_order: Mapped[Optional[str]] = mapped_column(String(50))                      # type: ignore[misc]

    song_book: Mapped["Song_Book"] = relationship(back_populates="song_book_items")     # type: ignore[misc]
    song: Mapped["Song"] = relationship(back_populates="song_book_items")               # type: ignore[misc]

    #verses: Mapped[List["Verse"]] = relationship(back_populates="song_book_item")       # type: ignore[misc]

'''
class Verse(Base):
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
    __tablename__: str = "verse"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    song_book_item_id: Mapped[int] = mapped_column(ForeignKey("song_book_item.id"))     # type: ignore[misc]

    type: Mapped[str] = mapped_column(String(1))                                        # type: ignore[misc]
    number: Mapped[int]                                                                 # type: ignore[misc]
    lyrics: Mapped[Optional[str]] = mapped_column(String(3000))                         # type: ignore[misc]

    song_book_item: Mapped["Song_Book_Item"] = relationship(back_populates="verses")    # type: ignore[misc]

    Index(
        "compound_index_verse",
            "song_book_item_id",
            "type",
            "number",
            unique=True,
    )
'''