from flask import Flask

from .extensions import db

from .commands import create_tables

from .routes import main

from .auth import auth

def create_app(config_file='settings.py'):
    app=Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    app.cli.add_command(create_tables)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app

