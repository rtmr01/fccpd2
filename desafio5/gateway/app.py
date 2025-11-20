from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

USERS_SERVICE_URL = "http://users-service:5001/api/users"
ORDERS_SERVICE_URL = "http://orders-service:5002/api/orders"

@app.route('/users', methods=['GET'])
def proxy_users():
    try:
        response = requests.get(USERS_SERVICE_URL, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro ao acessar Users Service: {e}"}), 503 

@app.route('/orders', methods=['GET'])
def proxy_orders():
    try:
        response = requests.get(ORDERS_SERVICE_URL, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro ao acessar Orders Service: {e}"}), 503 # Service Unavailable

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "API Gateway Funcionando.",
        "endpoints": {
            "/users": "Acessa o Microsserviço de Usuários",
            "/orders": "Acessa o Microsserviço de Pedidos"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)