from flask import render_template
from sqlmodel import Session, select
from prayer_of_hannah.main import bp
from prayer_of_hannah import get_dbe
import prayer_of_hannah.models as models


@bp.route('/')
def index():
    with Session(get_dbe()) as session:
        song_books = session.exec(select(models.Song_Book))
        return render_template('index.html', song_books = song_books)