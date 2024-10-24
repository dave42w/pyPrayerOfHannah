from typing import cast
from typing import List

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
import pytest

from dbs.models import Base
from dbs.models import Author, Song, Author_Song

@pytest.fixture
def dbe():
    def _dbe() -> Engine:
        e: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
        Base.metadata.create_all(e)
        return e
    return _dbe


def test_add_author_song(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        surname: str ="AddWarnock"
        first_names: str = "AddDave Z"
        display_name: str = f"{surname}, {first_names}"
        title: str ="AddAnd Can It Be"
        expected_len: int = 1

        author1: Author = Author(surname=surname, first_names=first_names, songs=[])
        session.add(author1)

        song1: Song = Song(title=title, authors=[])
        session.add(song1)

        author_song1: Author_Song = Author_Song(author=author1, song=song1)
        session.add(author_song1)
        session.commit()

        aid: int = author1.id
        sid: int = song1.id

        assert aid, f"AuthorId is {aid}"
        assert sid, f"SongId is {sid}"

        # check only 1 row in the 3 tables
        s1: ScalarResult[Author_Song] = session.scalars(select(Author_Song))
        l1 = len(s1.all())
        assert l1 == expected_len, f"Author_Song Count is {l1} should be {expected_len}"

        s2: ScalarResult[Author] = session.scalars(select(Author))
        l2 = len(s2.all())
        assert l2 == expected_len, f"Song Count is {l2} should be {expected_len}"

        s3: ScalarResult[Song] = session.scalars(select(Song))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Author Count is {l3} should be {expected_len}"

        # check from Author to Song
        s4: ScalarResult[Author] = session.scalars(select(Author).where(Author.id==aid))
        r4: Author = cast(Author, s4.first())
        assert r4.id == aid, "author id is {r4.id} should be {aid}"
        assert r4.surname == surname, "author Surname is {r4.surname} should be {surname}"
        assert r4.first_names == first_names, "author first_names is {r4.first_names} should be {first_names}"
        assert r4.display_name == display_name, "author display_name is {r4.display_name} should be {display_name}"
        assert r4.songs, "Should not have empty songs"

        author_songs: List[Author_Song] = r4.songs
        l4 = len(author_songs)
        assert l4 == expected_len, f"Count is {l4} should be {expected_len}"
        song: Song = author_songs[0].song
        assert song.title == title, f"Title is {song.title} should be {title}"

        # check from Song to Author
        s5: ScalarResult[Song] = session.scalars(select(Song).where(Song.id==sid))
        r5: Song = cast(Song, s5.first())
        assert r5.id == sid, "Song id is {r5.id} should be {sid}"
        assert r5.title == title, "song title is {r5.title} should be {title}"
        assert r5.authors, "Should not have empty authors"

        author_songs2: List[Author_Song] = r5.authors
        l5 = len(author_songs2)
        assert l5 == expected_len, f"Count is {l5} should be {expected_len}"
        author: Author = author_songs[0].author
        assert author.display_name == display_name, f"Display Name is {author.display_name} should be {display_name}"

def test_del_author_song(dbe) -> None:
    e: Engine = dbe()
    with Session(e) as session:
        surname: str ="DelWarnock"
        first_names: str = "DelDave Z"
        title: str ="DelAnd Can It Be"
        expected_len: int = 1

        author1: Author = Author(surname=surname, first_names=first_names, songs=[])
        session.add(author1)

        song1: Song = Song(title=title, authors=[])
        session.add(song1)

        author_song1: Author_Song = Author_Song(author=author1, song=song1)
        session.add(author_song1)
        session.commit()

        aid: int = author1.id
        sid: int = song1.id

        assert aid, f"AuthorId is {aid}"
        assert sid, f"SongId is {sid}"

        # check only 1 row in the 3 tables
        s1: ScalarResult[Author_Song] = session.scalars(select(Author_Song))
        l1 = len(s1.all())
        assert l1 == expected_len, f"Author_Song Count is {l1} should be {expected_len}"

        s2: ScalarResult[Author] = session.scalars(select(Author))
        l2 = len(s2.all())
        assert l2 == expected_len, f"Song Count is {l2} should be {expected_len}"

        s3: ScalarResult[Song] = session.scalars(select(Song))
        l3 = len(s3.all())
        assert l3 == expected_len, f"Author Count is {l3} should be {expected_len}"

        s4: ScalarResult[Author_Song] = session.scalars(select(Author_Song).where(Author_Song.author_id==aid, Author_Song.song_id==sid))
        r4: Author_Song = cast(Author_Song, s4.first())
        session.delete(r4)

        # check row counts after delete author_song
        s5: ScalarResult[Author_Song] = session.scalars(select(Author_Song))
        l5 = len(s5.all())
        assert not l5, f"Author_Song Count is {l5} should be {expected_len}"

        s6: ScalarResult[Author] = session.scalars(select(Author))
        l6 = len(s6.all())
        assert l6 == expected_len, f"Author Count is {l6} should be {expected_len}"

        s7: ScalarResult[Song] = session.scalars(select(Song))
        l7 = len(s7.all())
        assert l7 == expected_len, f"Song Count is {l7} should be {expected_len}"

        # check Songs is empty in Author
        s8: ScalarResult[Author] = session.scalars(select(Author).where(Author.id==aid))
        r8: Author = cast(Author, s8.first())
        assert not r8.songs, "Should have empty songs"

        # check Authors is empty in Songs
        s9: ScalarResult[Song] = session.scalars(select(Song).where(Song.id==sid))
        r9: Song = cast(Song, s9.first())
        assert not r9.authors, "Should have empty authors"
