from flask import Blueprint, jsonify, request
from models import Venda, ItemVenda, Pagamento, TipoPagamento, db

bp = Blueprint("vendas", __name__)


@bp.route("/venda", methods=["GET"])
def listar_vendas():
    vendas_totais = Venda.total()
    vendas_id = []
    vendas_filtradas = []

    for venda_total in vendas_totais:
        dic_venda_filtrada = {
                "id": venda_total["id"],
                "data_venda": venda_total["data"].strftime("%Y-%m-%d %H:%M:%S"),
                "total": venda_total["preco_item"] * venda_total["quantidade"],
                "produtos": [{
                    "livro": venda_total["livro"],
                    "quantidade": venda_total["quantidade"],
                    "preco_item": venda_total["preco_item"]
                }]
            }
        if dic_venda_filtrada["id"] in vendas_id:
            for venda in vendas_filtradas:
                if dic_venda_filtrada["id"] == venda["id"]:
                    venda["total"] += venda_total["preco_item"] * venda_total["quantidade"]
                    dic_produto = {
                        "livro": venda_total["livro"],
                        "quantidade": venda_total["quantidade"],
                        "preco_item": venda_total["preco_item"]
                    }
                    venda["produtos"].append(dic_produto)
        else:
            vendas_id.append(dic_venda_filtrada["id"])
            vendas_filtradas.append(dic_venda_filtrada)

    return jsonify(data=vendas_filtradas)


@bp.route("/venda", methods=["POST"])
def inserir_venda():
    try:
        dados_vendas = request.get_json()

        desconto = dados_vendas["desconto"]
        produtos = dados_vendas["produtos"]
        tipo_pagamento = dados_vendas["tipo_pagamento"]
        valor_total = dados_vendas["valor_total"]

        venda = Venda()

        venda.desconto = desconto
        db.session.add(venda)
        db.session.flush()

        pagamento = Pagamento()
        tipo_pagamento = TipoPagamento.query.filter_by(descricao=tipo_pagamento).first()

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

        return jsonify(msg="Venda concluida com sucesso"), 201
    except Exception as e:
        if isinstance(e, AttributeError):
            return jsonify(error="Livro não existe")
