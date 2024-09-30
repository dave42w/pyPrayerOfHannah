from flask import Blueprint

bp = Blueprint('services', __name__)


from prayer_of_hannah.services import routes