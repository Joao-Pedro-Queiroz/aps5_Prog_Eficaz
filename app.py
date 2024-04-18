from flask import Flask, request
from flask_pymongo import PyMongo


app = Flask("nome_da_minha_aplicacao")
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@cluster0.ac4lm23.mongodb.net/biblioteca_db"
mongo = PyMongo(app)


@app.route('/usuarios', methods=['GET'])
def get_all_users():
    filtro = {}
    projecao = {"_id": 0}
    dados_usuarios = mongo.db.usuarios_aps_5.find(filtro, projecao)

    resp = {
        "usuarios": list(dados_usuarios)
    }

    return resp, 200

@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():

    usuario = request.json

    mongo.db.usuarios_aps_5.insert_one(usuario)

    return {"mensagem": "Usuário adicionado com sucesso"}, 201

if __name__ == '__main__':
    app.run(debug=True)