from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_create_user():
    client = TestClient(app)  # arrange
    response = client.post(
        '/users/',  # act
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    # validar UserPublic
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }
