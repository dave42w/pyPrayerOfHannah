from flask import render_template
from prayer_of_hannah.live_worship import bp

@bp.route('/')
def index():
    return render_template('live_worship/index.html')
