from flask import Flask
from settings import app_config, app_active

from flask_sqlalchemy import SQLAlchemy

from .routes.livro import bp as bp_livro
from .routes.vendas import bp as bp_venda

config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('../settings.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    db.init_app(app)

    app.register_blueprint(bp_livro)
    app.register_blueprint(bp_venda)

    return app
