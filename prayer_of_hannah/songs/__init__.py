from flask import Blueprint

bp = Blueprint('songs', __name__)


from prayer_of_hannah.songs import routes