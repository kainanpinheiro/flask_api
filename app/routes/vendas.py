from flask import Blueprint, jsonify, request
from models import Venda, Item_Venda, db

bp = Blueprint("vendas", __name__)


@bp.route("/venda", methods=["POST"])
def inserir_venda():
    try:
        dados_vendas = request.get_json()

        desconto = dados_vendas["desconto"]
        produtos = dados_vendas["produtos"]

        venda = Venda()

        venda.desconto = desconto
        db.session.add(venda)
        db.session.flush()

        for produto in produtos:
            itens_venda = Item_Venda()
            itens_venda.venda_id = venda.id
            itens_venda.livro_id = produto["id"]
            itens_venda.quantidade = produto["quantidade"]
            itens_venda.preco_item = produto["preco_item"]

            db.session.add(itens_venda)
            db.session.flush()

        db.session.commit()

        return jsonify(Venda.to_dict(venda)), 201
    except Exception as e:
        print(e)
