from flask import render_template
from prayer_of_hannah.songs import bp

@bp.route('/')
def index():
    return render_template('songs/index.html')
