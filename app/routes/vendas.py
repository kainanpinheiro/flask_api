from flask import Blueprint, jsonify, request
from models import Venda, ItemVenda, Pagamento, TipoPagamento, db

bp = Blueprint("vendas", __name__)


@bp.route("/venda", methods=["GET"])
def listar_vendas():
    vendas_totais = Venda.total()
    return jsonify(vendas_totais)


@bp.route("/venda/<int:id>", methods=["GET"])
def uma_venda(id):
    venda = Venda.uma_venda(id)
    return jsonify(venda)


@bp.route("/venda", methods=["POST"])
def inserir_venda():
    try:
        dados_vendas = request.get_json()

        desconto = dados_vendas["desconto"]
        produtos = dados_vendas["produtos"]
        id_pagamento = dados_vendas["id_pagamento"]
        valor_total = dados_vendas["valor_total"]

        venda = Venda()

        venda.desconto = desconto
        db.session.add(venda)
        db.session.flush()

        pagamento = Pagamento()
        tipo_pagamento = TipoPagamento.query.filter_by(id=id_pagamento).first()

        pagamento.venda_id = venda.id
        pagamento.valor = valor_total
        pagamento.tipo_pagamento_id = tipo_pagamento.id
        db.session.add(pagamento)

        for produto in produtos:
            itens_venda = ItemVenda()
            itens_venda.venda_id = venda.id
            itens_venda.livro_id = produto["id"]
            itens_venda.quantidade = produto["quantidade"]
            itens_venda.preco_item = produto["preco_item"]

            db.session.add(itens_venda)

            venda_concluida = Venda.query.filter_by(id=venda.id).first()

            if venda_concluida is None:
                return jsonify(error="Algum livro está fora de estoque!")

        db.session.commit()
        db.session.close()

        return jsonify(msg="Venda concluida com sucesso"), 201
    except Exception as e:
        if isinstance(e, AttributeError):
            return jsonify(error="Livro não existe")
