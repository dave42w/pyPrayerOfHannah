from flask import Blueprint

bp = Blueprint('main', __name__)

from prayer_of_hannah.main import routes