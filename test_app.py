def test_routes(client):
    # test the root route
    response = client.get('/')
    assert response.status_code == 302  # expect a redirect
    assert response.location.endswith('/users')  # expect a redirect to /users

    # test the users route
    response = client.get('/users')
    assert response.status_code == 200  # expect a successful response
    assert b'Users' in response.data  # expect the "Users" text to be in the HTML response

def test_users_destroy(client, session):
    # Create a test user to delete
    user = User(first_name='Test', last_name='User')
    session.add(user)
    session.commit()
    
    # Send a POST request to delete the test user
    response = client.post(f'/users/{user.id}/delete')
    
    # Expect a redirect to the /users page
    assert response.status_code == 302
    assert response.location.endswith('/users')
    
    # Expect the test user to be deleted
    deleted_user = User.query.get(user.id)
    assert deleted_user is None
