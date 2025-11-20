from flask import Flask, jsonify
import requests
import socket

app = Flask(__name__)

USERS_SERVICE_URL = "http://users-service:5001/users"

@app.route('/summary')
def get_summary():
    try:
        response = requests.get(USERS_SERVICE_URL, timeout=5)
        response.raise_for_status() 
        users = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Não foi possível conectar ao Microsserviço de Usuários: {e}"}), 500

    active_users = []
    
    for user_id, data in users.items():
        if data['status'] == 'ativo':
            summary = f"Usuário {data['name']} (ID: {user_id}) ativo desde {data['since']}"
            active_users.append(summary)

    return jsonify({
        "status": "OK",
        "message": f"Dados processados pelo container: {socket.gethostname()}",
        "active_users_summary": active_users
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)