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
    id = usuario.get("id")

    filtro = {"id": id}
    projecao = {"_id": 0}
    cursor = mongo.db.usuarios_aps_5.find(filtro, projecao)
    
    # Convertendo o cursor em uma lista para facilitar a manipulação
    dados_usuarios = list(cursor)
    
    print(dados_usuarios)
    
    if len(dados_usuarios) > 0:
        return {"erro": "Usuário já cadastrado"}, 400

    mongo.db.usuarios_aps_5.insert_one(usuario)

    return {"mensagem": "Usuário adicionado com sucesso"}, 201


@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    try:
        filtro = {"id": str(id)}
        projecao = {"_id": 0}
        cursor = mongo.db.usuarios_aps_5.find(filtro, projecao)
        dados_usuarios = list(cursor)
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if len(dados_usuarios) == 0:
            return {"erro": "Usuário não encontrado"}, 404
        else:
            data = request.json
            novos_dados = {
                "$set": data
            }

            try:
                mongo.db.usuarios_aps_5.update_one(filtro, novos_dados)
            except:
                return {"erro": "Dados inválidos"}, 400

            return {"mensagem": "Usuário atualizado com sucesso"}, 200

@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    try:
        filtro = {"id": str(id)}
        projecao = {"_id": 0}
        dados_usuario = list(mongo.db.usuarios_aps_5.find(filtro, projecao))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_usuario:
            return {"usuarios": dados_usuario}, 200
        else:
            return {"erro": "Usuário não encontrado"}, 404

if __name__ == '__main__':
    app.run(debug=True)