from flask import Flask
from config import Config
from sqlalchemy.engine import Engine

from prayer_of_hannah import models
__all__ = ["models"]

from prayer_of_hannah.dbms import Dbms

__DB: Dbms | None = None
__DBE: Engine | None = None


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints here
    from prayer_of_hannah.main import bp as main_bp
    app.register_blueprint(main_bp)

    from prayer_of_hannah.live_worship import bp as live_worship_bp
    app.register_blueprint(live_worship_bp, url_prefix='/live')

    from prayer_of_hannah.services import bp as services_bp
    app.register_blueprint(services_bp, url_prefix='/services')

    from prayer_of_hannah.songs import bp as songs_bp
    app.register_blueprint(songs_bp, url_prefix='/songs')

    #@app.route('/test/')
    #def test_page():
    #    return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

def get_db() -> Dbms:
    global __DB
    if __DB is None:
        __DB = Dbms(False, Config.SQLALCHEMY_DATABASE_URI)
        __DB.create_database_structure()

    return __DB

def get_dbe() -> Engine:
    global __DBE
    if __DBE is None:
        __DBE = get_db().engine

    return __DBE
