import sys
sys.path.append('.')

from application import app

def test_hello_world():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == 'Hello, World!'
