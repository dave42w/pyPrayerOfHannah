from dbms import Dbms
from models import VerseType, Author, Song_Book, Song, Song_Book_Item, Verse
from sqlmodel import Session, select
import pytest
import pathlib as pl
from typing import Sequence

@pytest.fixture
def db() -> Dbms:
    dbase = Dbms(True)
    dbase.delete_database_file()
    dbase.create_database_structure()
    return dbase

def test_delete_database_test() -> None:
    db = Dbms()
    db.delete_database_file()
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
        results: Sequence[Author] = session.exec(select(Author).order_by(Author.surname, Author.first_names)).all()
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


def test_song_book(db) -> None:
    with Session(db.engine) as session:

        row: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")
        session.add(row)

        session.commit()

        assert row.id is not None, "Row should exist after add"
        assert row.id == 1, f"Add id should be 1: {row.id}"
        assert row.code == "StF", f"Add code should be 'StF': {row.code}"
        assert row.name == "Singing the Faith", "Add name should be 'Singing the Faith': {row.name}"
        assert row.url == "methodist.org", f"Add url should be 'methodist.org': {row.url}"


def test_song(db) -> None:
    with Session(db.engine) as session:
        author: Author = Author(surname="Wesley", first_names="John")
        song_book: Song_Book = Song_Book(code="StF", name="Singing the Faith", url="methodist.org")

        song: Song = Song(title="And Can it be",  authors=[author])

        song_book_item: Song_Book_Item = Song_Book_Item(song_book=song_book, song=song, nbr=345, verse_order="v1 c1 b1 v2 v3")

        lyrics1: str = "v1: And can it be that I should gain<br>"\
                       "an interest in the Saviour's blood?<br>"\
                       "Died he for me, who caused his pain?<br>"\
                       "For me, who him to death pursued?<br>"\
                       "Amazing love! How can it be<br>"\
                       "that thou, my God, shouldst die for me?<br>"

        lyrics2: str = "c1: 'Tis mystery all:the Immortal dies!<br>"\
                       "Who can explore his strange design?<br>"\
                       "In vain the first-born seraph tries<br>"\
                       "to sound the depths of love divine.<br>"\
                       "'Tis mercy all! Let earth adore,<br>"\
                       "let angel minds enquire no more.<br>"

        lyrics3: str = "b1: He left his Father's throne above --<br>"\
                       "so free, so infinite his grace --<br>"\
                       "emptied himself of all but love,<br>"\
                       "and bled for Adam's helpless race.<br>"\
                       "'Tis mercy all, immense and free;<br>"\
                       "for, O my God, it found out me!<br>"

        lyrics4: str = "v2: Long my imprisoned spirit lay<br>"\
                       "fast bound in sin and nature's night;<br>"\
                       "thine eye diffused a quickening ray --<br>"\
                       "I woke, the dungeon flamed with light,<br>"\
                       "my chains fell off, my heart was free,<br>"\
                       "I rose, went forth, and followed thee.<br>"

        lyrics5: str = "v3: No condemnation now I dread;<br>"\
                       "Jesus, and all in him, is mine!<br>"\
                       "Alive in him, my living Head,<br>"\
                       "and clothed in righteousness divine,<br>"\
                       "bold I approach the eternal throne,<br>"\
                       "and claim the crown, through Christ, my own.<br>"

        v1: Verse = Verse(type=VerseType.VERSE,  number=1, lyrics=lyrics1, song_book_item=song_book_item)
        v2: Verse = Verse(type=VerseType.CHORUS, number=1, lyrics=lyrics2, song_book_item=song_book_item)
        v3: Verse = Verse(type=VerseType.BRIDGE, number=1, lyrics=lyrics3, song_book_item=song_book_item)
        v4: Verse = Verse(type=VerseType.VERSE,  number=2, lyrics=lyrics4, song_book_item=song_book_item)
        v5: Verse = Verse(type=VerseType.VERSE,  number=3, lyrics=lyrics5, song_book_item=song_book_item)

        session.add(author)

        session.add(song_book)

        session.add(song)

        session.add(song_book_item)

        session.add(v1)
        session.add(v2)
        session.add(v3)
        session.add(v4)
        session.add(v5)

        session.commit()

    with Session(db.engine) as session:
        vc1: Verse | None = session.get(Verse, 1)
        assert vc1 is not None, "Get verse id 1 failed"
        assert isinstance(vc1, Verse), "Get verse id 1 didn't return a verse"
        if isinstance(vc1, Verse):
            assert vc1.type == VerseType.VERSE, f"Verse 1 type is incorrect: {vc1.type}"
            assert vc1.number == 1, f"Verse 1 number is incorrect: {vc1.number}"
            assert vc1.lyrics == lyrics1, f"Verse 1 lyrics incorrect: {vc1.lyrics}"
