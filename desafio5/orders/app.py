from flask import Flask, jsonify

app = Flask(__name__)
ORDERS_DATA = {
    "101": {"user_id": 1, "product": "Livro de Docker", "value": 49.90},
    "102": {"user_id": 2, "product": "Mouse Gamer", "value": 129.50},
    "103": {"user_id": 1, "product": "Curso Online", "value": 300.00}
}

@app.route('/api/orders')
def get_orders():
    return jsonify(ORDERS_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)