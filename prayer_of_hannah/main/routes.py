from flask import render_template
from prayer_of_hannah.main import bp


@bp.route('/')
def index():
    return render_template('index.html')