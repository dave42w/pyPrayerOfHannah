from flask import render_template
from sqlmodel import Session, select
from prayer_of_hannah.songs import bp
from prayer_of_hannah.models import Song
from prayer_of_hannah import db

@bp.route('/')
def index():
    with Session(db.engine) as session:
        songs = session.exec(select(Song).order_by(Song.title))
        return render_template('songs/index.html', songs = songs)
