from flask import render_template
from sqlmodel import Session, select
from prayer_of_hannah.songs import bp
from prayer_of_hannah.models import Song
from prayer_of_hannah import get_dbe

@bp.get('/')
def index():
    return render_template('songs/index.html')

@bp.get('/htmx/songs')
def songs():
    with Session(get_dbe()) as session:
        songs = session.exec(select(Song).order_by(Song.title))
        return render_template('songs/songs.html', songs = songs)
