import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

livros = [
    {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis", "preco": 29.90},
    {"id": 2, "titulo": "O Cortiço", "autor": "Aluísio Azevedo", "preco": 34.50},
    {"id": 3, "titulo": "Memórias Póstumas de Brás Cubas", "autor": "Machado de Assis", "preco": 39.90},
]
proximo_id = 4


@app.get("/")
def inicio():
    return jsonify({"mensagem": "API da Livraria funcionando", "rotas": ["GET /livros", "POST /livros", "DELETE /livros/<id>"]})


@app.get("/livros")
def listar_livros():
    return jsonify(livros)


@app.post("/livros")
def cadastrar_livro():
    global proximo_id
    dados = request.get_json(silent=True) or {}
    titulo = str(dados.get("titulo", "")).strip()
    autor = str(dados.get("autor", "")).strip()
    try:
        preco = float(dados.get("preco", ""))
    except (TypeError, ValueError):
        return jsonify({"erro": "O preço deve ser um número válido."}), 400
    if not titulo or not autor or preco < 0:
        return jsonify({"erro": "Informe título, autor e preço não negativo."}), 400
    livro = {"id": proximo_id, "titulo": titulo, "autor": autor, "preco": round(preco, 2)}
    proximo_id += 1
    livros.append(livro)
    return jsonify(livro), 201


@app.delete("/livros/<int:livro_id>")
def excluir_livro(livro_id):
    livro = next((livro for livro in livros if livro["id"] == livro_id), None)
    if livro is None:
        return jsonify({"erro": "Livro não encontrado."}), 404
    livros.remove(livro)
    return jsonify({"mensagem": "Livro excluído com sucesso."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
