from flask import Flask

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from settings import app_config, app_active

config = app_config[app_active]

if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
else:
    db = SQLAlchemy(config.APP)


item_venda = db.Table(
    "item_venda",
    db.Column("livro_id", db.Integer, db.ForeignKey("livro.id"), primary_key=True),
    db.Column("venda_id", db.Integer, db.ForeignKey("venda.id"), primary_key=True),
    db.Column("quantidade", db.Integer, nullable=False),
    db.Column("preco_item", db.Float, nullable=False),
)


class Livro(db.Model):
    __tablename__ = "livro"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True, nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(25), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(100), nullable=False)

    items_venda = db.relationship(
        "Venda",
        secondary=item_venda,
        backref=db.backref("items_da_venda", lazy="dynamic"),
    )

    def to_dict(livro):
        livro_dic = {}
        livro_dic = {
            "titulo": livro.titulo,
            "autor": livro.autor,
            "editora": livro.editora,
            "isbn": livro.isbn,
            "categoria": livro.categoria,
            "preco": livro.preco,
            "estoque": livro.estoque,
            "foto": livro.foto
        }

        return livro_dic


class Venda(db.Model):
    __tablename__ = "venda"

    id = db.Column(db.Integer, primary_key=True)
    desconto = db.Column(db.Float, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)


if __name__ == "__main__":
    manager.run()
