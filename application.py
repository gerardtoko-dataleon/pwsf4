from flask import Flask, request, jsonify
from functools import wraps

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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
