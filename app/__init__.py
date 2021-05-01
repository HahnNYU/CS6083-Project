from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    # instantiate the app
    app=Flask(__name__)

    # set config
    app.config.from_object(config_class)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    return app
