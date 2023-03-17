def test_routes(client):
    # test the root route
    response = client.get('/')
    assert response.status_code == 302
    assert response.location.endswith('/users')

    # test the users route
    response = client.get('/users')
    assert response.status_code == 200
    assert b'Users' in response.data


def test_users_destroy(client, session):

    user = User(first_name='Test', last_name='User')
    session.add(user)
    session.commit()

    response = client.post(f'/users/{user.id}/delete')

    assert response.status_code == 302
    assert response.location.endswith('/users')

    deleted_user = User.query.get(user.id)
    assert deleted_user is None
