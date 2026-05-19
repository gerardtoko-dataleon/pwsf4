from flask import Flask, request, jsonify
from functools import wraps
# import json
from models.user import get_db
from models.user import (
    create_user, get_user_by_username, get_user_by_id, update_user, delete_user
)
app = Flask(__name__)

GLOBAL_API_KEY = "api-key-123"
def auth_wrapper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != GLOBAL_API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/blogs', methods=['POST'])
@auth_wrapper
def blog_articles():
    data = request.get_json()
    
    # users = []
    # with open('users.json', 'r') as f:
    #     users = json.load(f)

    # with open('users.json', 'w') as f:
    #     json.dump(data, f)

    return jsonify(data), 201

@app.route('/blog/<post_id>', methods=['GET'])
@auth_wrapper
def blog_article(post_id):
    return f'Hello, World! {post_id}'

@app.route('/calculator', methods=['POST'])
@auth_wrapper
def calculator():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    return a * b
    

# CRUD Users
@app.route('/users', methods=['GET'])
@auth_wrapper
def list_users():
    # Simple listing (pour démo, pas paginé)
    conn = get_db()
    users = conn.execute('SELECT id, username FROM users').fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@app.route('/users', methods=['POST'])
@auth_wrapper
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return 'Champs manquants', 400
    if get_user_by_username(username):
        return 'Utilisateur déjà existant', 409
    create_user(username, password)
    return 'Utilisateur créé', 201

@app.route('/users/<int:user_id>', methods=['GET'])
@auth_wrapper
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return 'Utilisateur non trouvé', 404
    return jsonify(dict(user))

@app.route('/users/<int:user_id>', methods=['PUT'])
@auth_wrapper
def update_user_route(user_id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return 'Champs manquants', 400
    update_user(user_id, username, password)
    return 'Utilisateur modifié', 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
@auth_wrapper
def delete_user_route(user_id):
    delete_user(user_id)
    return 'Utilisateur supprimé', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
