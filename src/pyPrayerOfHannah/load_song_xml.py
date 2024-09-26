import xmltodict # type: ignore
import os
from dbms import Dbms
from sqlmodel import Session, select
from models import Author, Song_Book, Song, Song_Book_Item, Verse

#PATH_TO_XML = 'resources'
PATH_TO_XML = 'xml'

def get_list_items(list_items) -> list:
    result: list = []
    if isinstance(list_items, str):
        result = [list_items]
    else:
        for item in list_items:
            if result.__len__() >= 1:
                result.append(item)
            else:
                result = [item]
    return result

def get_titles(xml_dict) -> list:
    return get_list_items(xml_dict['song']['properties']['titles']['title'])

def get_verse_order(xml_dict) -> str:
    return xml_dict['song']['properties']['verseOrder']

def get_authors(xml_dict) -> list:
    return get_list_items(xml_dict['song']['properties']['authors']['author'])

def get_song_books(xml_dict) -> list:
    song_books = xml_dict['song']['properties']['songbooks']['songbook']
    result: list = []

    book: str = ''
    nbr: str = ''
    sb: list = []

    if isinstance(song_books, dict):
        book = str(song_books.get('@name'))
        nbr = str(song_books.get('@entry'))
        sb = [book, nbr]
        result = [sb]
    else:
        for item in song_books:
            book = item.get('@name')
            nbr = item.get('@entry')
            sb = [book, nbr]
            if len(result) >= 1:
                result.append(sb)
            else:
                result = [sb]

    return result

def get_verses(xml_dict) -> list:
    verses = xml_dict['song']['lyrics']['verse']

    result: list = []
    verse_code: str =''
    verse_lines: str =''
    verse: list = []

    if isinstance(verses, dict):
        #print('Dict verses:', end='')
        verse_code = str(verses.get('@name'))
        #print(f'{verse_code}')
        verse_lines = str(verses.get('#text'))
        #print(f'{lines}')
        verse = [verse_code, verse_lines]
        result = [verse]
    else:
        for v in verses:
            #print('list verses:', end='')
            verse_code = str(v.get('@name'))
            #print(f'{verse_code}')
            verse_lines = str(v.get('#text'))
            #print(f'{lines}')
            verse = [verse_code, verse_lines]

            if len(result) >= 1:
                result.append(verse)
            else:
                result = [verse]

    return result

def save_authors(session: Session, authors: list) -> list:
        result = []
        for author in authors:
            names: list = author.split()
            sn: str = names[-1].strip()
            fn: str = ''
            for n in names[0:-1]:
                if len(fn) >= 1:
                    fn = ' ' + n
                else:
                    fn = n
            fn = fn.strip()
            author_check: Author | None = session.exec(select(Author).where(Author.surname == sn).where(Author.first_names == fn)).first()
            if author_check is None:
                a: Author = Author(surname=sn, first_names=fn)

                session.add(a)
                result.append(a)
                #print(f'Saving author:{a}')
            else:
                pass
                #print(f'NOT Saving author:{fn} {sn}')
        return result

def save_song(session: Session, titles: list, authors: list) -> Song:
    song_check: Song | None = session.exec(select(Song).where(Song.title == titles[0])).first()
    if song_check is None:
        song: Song = Song(title=titles[0], authors=authors)

        session.add(song)
        return Song
    else:
        print(f'Duplicate so NOT Saving song:{titles[0]}')
        return None

def save_song_books(session: Session, song_books: list) -> None:
    for sb in song_books:
        sb_bk = sb[0].strip()
        song_book_check: Song_Book | None = session.exec(select(Song_Book).where(Song_Book.code == sb_bk)).first()
        if song_book_check is None:
            song_book: Song_Book = Song_Book(code=sb_bk, name=sb_bk)
            session.add(song_book)

def save_song_book_item(session: Session, titles: list, song_books: list, verse_code: str) -> None:
    for sb in song_books:
        sb_bk = sb[0].strip()
        sb_nbr = sb[1].strip()
        song_book: Song_Book | None = session.exec(select(Song_Book).where(Song_Book.code == sb_bk)).first()
        if song_book is not None:

            song: Song | None = session.exec(select(Song).where(Song.title == titles[0])).first()
            if song is not None:

                statement = select(Song_Book_Item).where(Song_Book_Item.song_book == song_book).where(Song_Book_Item.song == song)
                song_book_item_check: Song_Book_Item | None = session.exec(statement).first()
                if song_book_item_check is None:
                    if sb_nbr == "None":
                        song_book_item: Song_Book_Item = Song_Book_Item(song_book=song_book, song=song, verse_order = verse_code)
                        session.add(song_book_item)
                    else:
                        song_book_item = Song_Book_Item(song_book=song_book, song=song, nbr=sb_nbr, verse_order = verse_code)
                        session.add(song_book_item)

def save_verses(session: Session, titles: list, song_books: list, verses: list) -> None:
    for sb in song_books:
        sb_bk = sb[0].strip()
        song_book: Song_Book | None = session.exec(select(Song_Book).where(Song_Book.code == sb_bk)).first()
        if song_book is not None:

            song: Song | None = session.exec(select(Song).where(Song.title == titles[0])).first()
            if song is not None:

                statement = select(Song_Book_Item).where(Song_Book_Item.song_book == song_book).where(Song_Book_Item.song == song)
                song_book_item_check: Song_Book_Item | None = session.exec(statement).first()
                if song_book_item_check is not None:
                    for verse in verses:
                        vn: str = verse[0]
                        lyric: str = verse[1]

                        vt: str = vn[0]
                        if vt != "o":
                            if vt not in "vcbe":
                                print(f"Invalid Verse type for Song: {song}")

                            nbr: int = int(vn[1])

                            lines: list = lyric.split("\n")
                            br_lyric: str = ''
                            for li in lines:
                                if len(br_lyric) >= 1:
                                    br_lyric = br_lyric + "<br>" + li
                                else:
                                    br_lyric = li

                            verse_check: Verse | None = session.exec(select(Verse).where(Verse.song_book_item == song_book_item_check)).first()

                            if verse_check is None:
                                v: Verse = Verse(song_book_item=song_book_item_check, type=vt, number=nbr, lyrics=br_lyric)
                                session.add(v)


def main() -> None:
    db = Dbms()
    db.create_database_structure()

    # Scan the directory and get
    # an iterator of os.DirEntry objects
    # corresponding to entries in it
    # using os.scandir() method
    obj = sorted(os.scandir(PATH_TO_XML), key=lambda entry: entry.name)

    file_number: int = 0
    # List all files and directories in the specified path
    print("Files in '% s':" % PATH_TO_XML)
    for file in obj:
        if file.is_file():
            file_number += 1
            #print(f'{file_number}', end='')

            with open(PATH_TO_XML+'/'+file.name) as f:
                xml_string = f.read()

                xml_dict = xmltodict.parse(xml_string)

                titles: list = get_titles(xml_dict)
                #print(f'{titles}', end='')

                verse_order: str = get_verse_order(xml_dict)
                #print(f'#{verse_order}', end='')

                authors: list = get_authors(xml_dict)
                #print(f'#{authors}', end='')

                song_books: list = get_song_books(xml_dict)
                #print(f'#{song_books}', end='')
                #print('')

                verses: list = get_verses(xml_dict)
                #print(f'#{verses}')

                with Session(db.engine) as session:
                    model_authors: list = save_authors(session, authors)
                    save_song(session, titles, model_authors)
                    save_song_books(session, song_books)
                    session.commit()

                with Session(db.engine) as session:
                    save_song_book_item(session, titles, song_books, verse_order)
                    session.commit()

                with Session(db.engine) as session:
                    save_verses(session, titles, song_books, verses)
                    session.commit()

    print("end")


if __name__ == "__main__":
    main()
