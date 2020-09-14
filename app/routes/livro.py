from flask import Blueprint, jsonify, request
from app.models import Livro, db

bp = Blueprint("livro", __name__)


@bp.route("/livro", methods=["GET"])
def todos_livros():
    total_livros = []
    livros = Livro.query.all()

    for livro in livros:
        total_livros.append(Livro.to_dict(livro))

    return jsonify(data=total_livros)


@bp.route("/livro/<int:livro_id>", methods=["GET"])
def um_livro(livro_id):
    try:
        livro = Livro.query.filter_by(id=livro_id).first()

        if livro is None:
            return jsonify("Livro não existe!")

        return jsonify(Livro.to_dict(livro))
    except Exception as e:
        print(e)
        return jsonify("Error"), 404


@bp.route("/livro", methods=["POST"])
def inserir_novo_livro():
    try:
        dados_livro = request.get_json()
        livro = Livro(**dados_livro)

        db.session.add(livro)
        db.session.commit()

        return jsonify(Livro.to_dict(livro)), 201

    except Exception as e:
        print(e)
        return jsonify("Erro ao tentar inserir o livro"), 404


@bp.route('/livro/<int:livro_id>', methods=["PUT"])
def alterar_livro(livro_id):
    try:
        livro = Livro.query.filter_by(id=livro_id).first()

        livro.titulo = request.json.get('titulo')
        livro.autor = request.json.get('autor')
        livro.editora = request.json.get('editora')
        livro.isbn = request.json.get('isbn')
        livro.categoria = request.json.get('categoria')
        livro.preco = request.json.get('preco')
        livro.estoque = request.json.get('estoque')
        livro.foto = request.json.get('foto')

        db.session.commit()

        return jsonify(Livro.to_dict(livro)), 200
    except Exception as e:
        print(e)
        return jsonify("Erro ao tentar alterar o livro"), 404


@bp.route('/livro/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    try:
        livro = Livro.query.filter_by(id=livro_id).first()

        db.session.delete(livro)
        db.session.commit()

        return jsonify(), 200
    except Exception as e:
        print(e)
        return jsonify("Erro ao tentar deletar o livro"), 404
