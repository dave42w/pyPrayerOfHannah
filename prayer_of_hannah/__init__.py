from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config

from sqlmodel import Session

from prayer_of_hannah.dbms import Dbms
from prayer_of_hannah.models import Author, Song_Book

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db = Dbms()
    db.create_database_structure()
    dbe = db.engine
    #db.init_app(app)

    # Initialize Flask extensions here
    admin = Admin(app, name='PrayerOfHannah Admin')
    #admin = Admin(app, name='PrayerOfHannah Admin', theme=Bootstrap4Theme(swatch='cerulean'))
    # Add administrative views here
    admin.add_view(ModelView(Author, Session(dbe)))
    admin.add_view(ModelView(Song_Book, Session(dbe)))

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