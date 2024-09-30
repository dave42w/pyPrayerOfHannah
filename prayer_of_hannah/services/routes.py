from flask import render_template
from prayer_of_hannah.services import bp

@bp.route('/')
def index():
    return render_template('services/index.html')
