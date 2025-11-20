from flask import Flask, jsonify

app = Flask(__name__)
USERS_DATA = {
    "1": {"id": 1, "name": "Alice Silva", "email": "alice@ex.com"},
    "2": {"id": 2, "name": "Bruno Costa", "email": "bruno@ex.com"}
}

@app.route('/api/users')
def get_users():
    return jsonify(USERS_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)