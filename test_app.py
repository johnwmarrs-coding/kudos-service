# test_app.py

from app import app, db, Kudos, AppToken
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def init_database():
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_example():
    # This is just an example to prove that the tests are working
    assert True


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'The kudos-service is running!'


def test_overview_route(client, init_database):
    # Test overview route
    response = client.get('/kudos')
    assert response.status_code == 200
    assert response.json == []


def test_kudos_route(client, init_database):
    path = 'example'
    # Test POST method on /kudos route
    response = client.post(
        f"/kudos/{path}", json={'token': 'valid_token', 'title': 'Test Title', 'description': 'Test Description'})
    assert response.status_code == 401  # Unauthorized without valid token

    # Add a valid token to the database
    db.session.add(AppToken(token='valid_token'))
    db.session.commit()

    # Test POST method on /kudos route with valid token
    response = client.post(
        f"/kudos/{path}", json={'token': 'valid_token', 'title': 'Test Title', 'description': 'Test Description'})
    assert response.status_code == 200
    assert 'path' in response.json
    assert 'title' in response.json
    assert 'description' in response.json

    # Test GET method on /kudos/<path> route
    response = client.get(f'/kudos/{path}')
    assert response.status_code == 200
    assert response.json['path'] == path

    # Test PATCH method on /kudos/<path> route
    response = client.patch(f'/kudos/{path}')
    assert response.status_code == 200
    assert response.json['kudos'] == 1  # Kudos count increased by 1

    # Test DELETE method on /kudos/<path> route
    response = client.delete(f'/kudos/{path}', json={'token': 'valid_token'})
    assert response.status_code == 200
    assert response.data == b'Kudos deleted successfully'
