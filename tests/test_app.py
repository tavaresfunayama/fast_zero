from http import HTTPStatus


def test_create_user(client):
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


def test_read_user(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'testusername', 'email': 'test@test.com', 'id': 1}
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': '123',
            'username': 'testusername',
            'email': 'test@test.com',
            'id': 1,
        },
    )
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete(client):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}
