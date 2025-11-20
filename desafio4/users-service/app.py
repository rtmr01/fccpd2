from flask import Flask, jsonify
import socket
import json

app = Flask(__name__)
USERS_DATA = {
    1: {"name": "Alice Silva", "status": "ativo", "since": "2023-01-15"},
    2: {"name": "Bruno Costa", "status": "inativo", "since": "2024-05-20"},
    3: {"name": "Carla Mendes", "status": "ativo", "since": "2022-11-01"}
}

@app.route('/users')
def get_users():
    print(f"[{socket.gethostname()}] Requisição recebida em /users.")
    return jsonify(USERS_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)