from flask import Flask

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy, event

from datetime import datetime

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


class ItemVenda(db.Model):
    __tablename__ = "item_venda"

    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"), nullable=False)
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_item = db.Column(db.Float, nullable=False)

    livro = db.relationship("Livro", backref="item_venda")
    venda = db.relationship("Venda", backref="item_venda")

    @event.listens_for(db.session, "before_flush")
    def reduzir_estoque(*args):
        objetos = args[0]

        for objeto in objetos.new:
            if not isinstance(objeto, ItemVenda):
                continue

            livro = Livro.query.filter_by(id=objeto.livro_id).first()

            if livro.estoque >= objeto.quantidade:
                livro.estoque -= objeto.quantidade
                db.session.add(livro)
            else:
                db.session.close()


class Pagamento(db.Model):
    __tablename__ = "pagamento"

    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    tipo_pagamento_id = db.Column(db.Integer, db.ForeignKey('tipo_pagamento.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    venda = db.relationship("Venda", backref="pagamento")
    tipo_pagamento = db.relationship("TipoPagamento", backref="pagamento")


class TipoPagamento(db.Model):
    __tablename__ = "tipo_pagamento"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)


class Livro(db.Model):
    __tablename__ = "livro"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(25), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(255), nullable=False)

    def to_dict(livro):
        livro_dic = {}
        livro_dic = {
            "id": livro.id,
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
    data = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def total():
        vendas = Venda.query.order_by(Venda.data.desc()).all()
        vendas_totais = []

        for venda in vendas:
            venda_uma = Venda.uma_venda(venda.id)
            vendas_totais.append(venda_uma)
        db.session.close()
        return vendas_totais

    def uma_venda(venda_id):
        venda = Venda.query.filter_by(id=venda_id).first()
        dic_venda = {
                "id": venda.id,
                "data": venda.data.strftime("%Y-%m-%d %H:%M:%S"),
                "desconto": venda.desconto,
                "produtos": [],
                "total": -venda.desconto
                }
        for item in venda.item_venda:
            produtos = {
                    "livro": item.livro.titulo,
                    "quantidade": item.quantidade,
                    "preco_item": item.preco_item
                }
            dic_venda["total"] += produtos["preco_item"] * produtos["quantidade"]
            dic_venda["produtos"].append(produtos)
        for paga in venda.pagamento:
            dic_venda["tipo_pagamento"] = paga.tipo_pagamento.descricao
        db.session.close()
        return dic_venda


if __name__ == "__main__":
    manager.run()
