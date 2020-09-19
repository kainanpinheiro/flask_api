from flask import Blueprint, jsonify, request
from models import Venda, Item_Venda, db

bp = Blueprint("vendas", __name__)


@bp.route("/venda", methods=["GET"])
def listar_vendas():
    vendas_totais = Venda.total()
    vendas_id = []
    vendas_filtradas = []

    for venda_total in vendas_totais:
        dic_venda_filtrada = {
                "id": venda_total["id"],
                "data": venda_total["data"],
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

            venda_concluida = Venda.query.filter_by(id=venda.id).first()

            if venda_concluida is None:
                return jsonify("Algum livro está fora de estoque!")

            db.session.flush()

        db.session.commit()

        return jsonify("Venda concluída."), 201
    except Exception as e:
        return e
