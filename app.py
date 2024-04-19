from flask import Flask, request
from flask_pymongo import PyMongo
import os

app = Flask("nome_da_minha_aplicacao")
app.config["MONGO_URI"] = os.getenv("string_conexao_MongoDB_biblioteca")
mongo = PyMongo(app)


@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    usuario = request.json
    id = usuario.get("id", "")
    nome = usuario.get("nome", "")
    cpf = usuario.get("cpf", "")
    data_nascimento = usuario.get("data_nascimento", "")

    if not id or not nome or not cpf or not data_nascimento:
        return {"error": "Id, nome, cpf e data de nascimento são obrigatórios"}, 400
    
    if mongo.db.usuarios_aps_5.find_one(filter={"id": id}):
        return {"error": "Id já existe"}, 409
    
    if mongo.db.usuarios_aps_5.find_one(filter={"cpf": cpf}):
        return {"error": "CPF já existe"}, 409

    mongo.db.usuarios_aps_5.insert_one(usuario)

    return {"mensagem": "Usuário adicionado com sucesso"}, 201


@app.route('/usuarios', methods=['GET'])
def get_all_users():
    filtro = {}
    projecao = {"_id": 0}
    dados_usuarios = mongo.db.usuarios_aps_5.find(filtro, projecao)

    resp = {
        "usuarios": list(dados_usuarios)
    }

    return resp, 200


@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    try:
        filtro = {"id": id}
        projecao = {"_id": 0}
        dados_usuario = list(mongo.db.usuarios_aps_5.find(filtro, projecao))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_usuario:
            return {"usuarios": list(dados_usuario)}, 200
        else:
            return {"erro": "Usuário não encontrado"}, 404


@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    try:
        filtro = {"id": id}
        cursor = mongo.db.usuarios_aps_5.find(filtro)
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


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        filtro = {"id": id}
        dados_usuario = list(mongo.db.usuarios_aps_5.find(filtro))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_usuario:
            mongo.db.usuarios_aps_5.delete_one(filtro)
            return {"mensagem": "Usuário deletado com sucesso"}, 200
        else:
            return {"erro": "Usuário não encontrado"}, 404

#CRUD BIKES

@app.route('/bikes', methods=['POST'])
def adicionar_bicicleta():
    bicicleta = request.json
    id = bicicleta.get("id")
    marca = bicicleta.get("marca", "")
    modelo = bicicleta.get("modelo", "")
    cidade_alocada = bicicleta.get("cidade_alocada", "")

    if not id or not marca or not modelo or not cidade_alocada:
        return {"error": "Id, marca, modelo e cidade alocada são obrigatórios"}, 400
    
    if mongo.db.bicicletas_aps_5.find_one({"id": id}):
        return {"error": "Id já existe"}, 409

    mongo.db.bicicletas_aps_5.insert_one(bicicleta)

    return {"mensagem": "Bicicleta adicionado com sucesso"}, 201


@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    filtro = {}
    projecao = {"_id": 0}
    dados_bicicletas = mongo.db.bicicletas_aps_5.find(filtro, projecao)

    resp = {
        "bicicletas": list(dados_bicicletas)
    }

    return resp, 200

@app.route('/bikes/<int:id>', methods=['GET'])
def obter_bicicleta(id):
    try:
        filtro = {"id": id}
        projecao = {"_id": 0}
        dados_bicicleta = list(mongo.db.bicicletas_aps_5.find(filtro, projecao))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_bicicleta:
            return {"bicicletas": list(dados_bicicleta)}, 200
        else:
            return {"erro": "Bicicleta não encontrada"}, 404

@app.route('/bikes/<int:id>', methods=['PUT'])
def editar_bicicleta(id):
    try:
        filtro = {"id": id}
        cursor = mongo.db.bicicletas_aps_5.find(filtro)
        dados_bicicletas = list(cursor)
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if len(dados_bicicletas) == 0:
            return {"erro": "Bicicleta não encontrada"}, 404
        else:
            data = request.json
            novos_dados = {
                "$set": data
            }

            try:
                mongo.db.bicicletas_aps_5.update_one(filtro, novos_dados)
            except:
                return {"erro": "Dados inválidos"}, 400

            return {"mensagem": "Bicicleta atualizada com sucesso"}, 200


@app.route('/bikes/<int:id>', methods=['DELETE'])
def deletar_bicicleta(id):
    try:
        filtro = {"id": id}
        dados_bicicleta = list(mongo.db.bicicletas_aps_5.find(filtro))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_bicicleta:
            mongo.db.bicicletas_aps_5.delete_one(filtro)
            return {"mensagem": "Bicicleta deletada com sucesso"}, 200
        else:
            return {"erro": "Bicicleta não encontrada"}, 404


if __name__ == '__main__':
    app.run(debug=True)