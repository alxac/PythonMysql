import os
from flask import Flask, request
from flask_cors import CORS
from conexao import inserirTb, getPorID, getTodos, getDel, getEdit
from model import Usuario

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route("/", methods=['GET'])
def index():
    return "<h1>Hello World!</h1>"

@app.route("/deploy", methods=['GET'])    
def deploy():
    return "<h1>Testando deploy GitHub x Heroku </h1>"

## CREATE / inserir
@app.route('/user', methods=["POST"])
def cadastraUser():
    body = request.get_json()

    usuario = Usuario()
    usuario.name = body["name"]
    usuario.email = body["email"]
    print(usuario)

    if("name" not in body): return geraResponse(400, "O campo nome é obrigatório")
    if("email" not in body): return geraResponse(400, "O campo email é obrigatório")

    inserirTb(usuario)
    return geraResponse(200, "Usuario criado")

## CREATE / edit
@app.route('/user', methods=["PUT"])
def EditaUser():
    body = request.get_json()
    print(body)
    if("name" not in body): return geraResponse(400, "O campo nome é obrigatório")
    if("email" not in body): return geraResponse(400, "O campo email é obrigatório")

    getEdit(body["name"], body["email"], body["id"] )
    return geraResponse(200, "Usuario atualizado")

## SELECT ALL
@app.route('/user', methods=["GET"])
def GetAll():
    return geraResponse(200, "Listagem", getTodos())

## SELECT ID
@app.route('/user/<string:id>', methods=["GET"])
def GetById(id):
    return geraResponse(200, "Sucesso", getPorID(id))

## DELETE ID
@app.route('/user/<string:id>', methods=["DELETE"])
def GetDelId(id):
    return geraResponse(200, "Sucesso", getDel(id))

def geraResponse(status, msg, conteudo=False):
    response = {}
    response["status"] = status
    response["mensagem"] = msg

    if(conteudo):
        response["data"] = conteudo

    return response
########################################

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()