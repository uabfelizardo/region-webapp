from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from importlib import import_module
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    @app.before_request
    def create_tables():
        if not db.engine.table_names():
            db.create_all()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app