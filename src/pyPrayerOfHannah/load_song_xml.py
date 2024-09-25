import xmltodict # type: ignore
import os 
import db
from sqlmodel import Session

PATH_TO_XML = 'resources'

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

def save_authors(session: Session, authors: list) -> None:
        for author in authors:
            names: list = author.split()
            n: str = names[-1] + ','
            for na in names[0:-1]:
                n = n + ' ' + na
                a = db.Author(name=n)
            session.add(a)
            print(f'Saving author:{a}')


def main() -> None:
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
            print(f'{file_number}', end='')
            
            with open(PATH_TO_XML+'/'+file.name) as f:
                xml_string = f.read()
            
                xml_dict = xmltodict.parse(xml_string)

                titles: list = get_titles(xml_dict)
                print(f'{titles}', end='')

                verse_order: str = get_verse_order(xml_dict) 
                print(f'#{verse_order}', end='')

                authors: list = get_authors(xml_dict)
                print(f'#{authors}', end='')

                song_books: list = get_song_books(xml_dict)
                print(f'#{song_books}', end='')
                print('')

                verses: list = get_verses(xml_dict)
                print(f'#{verses}')

                with Session(db.ENGINE) as session:
                    save_authors(session, authors)
                    save_song_books(session, song_books)
                    save_songs(sess)

    print("end")


if __name__ == "__main__":
    main()
