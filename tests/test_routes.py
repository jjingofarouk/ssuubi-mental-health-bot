import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_chat_route(client):
    response = client.post('/api/chat', json={"session_id": "123", "message": "Hello"})
    assert response.status_code == 200