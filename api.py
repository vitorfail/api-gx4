from orm import ORM
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
postgres = ORM()
@app.route('/', methods=['GET'])
def tentativa():
    return jsonify({"status": "ok","message": "Não usamos essa rota:)"}), 200

@app.route('/register', methods=['POST'])
def registrar():
    postgres.iniciar()
    data = request.get_json()
    if "user" in data and "password" in data:
        if data["user"] != None and data["user"] != "" and data["password"] != None and data["password"] != "":
            verificar =postgres.verificar_user(data["user"])
            if verificar:
                postgres.registrar(data["user"], data["password"])  
                postgres.logout()
                return jsonify({"status": "ok","message": "Usuário cadastrado"}), 200
            else:
                postgres.logout()
                return jsonify({"status": "error","message": "USER EXIST"}), 200
        else:
            postgres.logout()
            return jsonify({"status": "error","message": "VAZIO"}), 200
    else:
        postgres.logout()
        return jsonify({"status": "error","message": "NO USER"}), 200

@app.route('/login', methods=['POST'])
def login():
    postgres.iniciar()
    data = request.get_json()
    if "user" in data and "password" in data:
        if data["user"] != None and data["user"] != "" and data["password"] != None and data["password"] != "":
            verificar =postgres.select_user_password(data["user"], data["password"])
            if len(verificar) >0:
                postgres.registrar(data["user"], data["password"])  
                postgres.logout()
                return jsonify({"status": "ok","message": "Checked"}), 200
            else:
                postgres.logout()
                return jsonify({"status": "error","message": "LOGIN ERR"}), 200
        else:
            postgres.logout()
            return jsonify({"status": "error","message": "VAZIO"}), 200
    else:
        postgres.logout()
        return jsonify({"status": "error","message": "NO USER"}), 200


if __name__ == '__main__':
    app.run(debug=True)