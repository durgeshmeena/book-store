import pytest
from app import app, db
from app.models import Member, Book
from flask_mongoengine import MongoEngine
from mongoengine import connect, disconnect
import mongomock

@pytest.fixture(scope="function", autouse=True)
def test_app():
    # update app config for testing
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        MONGODB_SETTINGS={
            'db': 'mydatabase',
            'host': 'mongodb://localhost',
            'mongo_client_class': mongomock.MongoClient,
            'uuidRepresentation': 'standard'
        }
    )

    disconnect()
    db = MongoEngine(app)
    yield
    disconnect()


@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client


def test_signup(test_client):
    # get signup page
    response = test_client.get('/signup')
    assert response.status_code == 200
    assert b"SignUp" in response.data

    # signup without username
    response = test_client.post('/signup', data={
        'name': 'invalid Test User',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert b"Username is required." in response.data

    # signup with invalid user name
    response = test_client.post('/signup', data={
        'name': 'invalid Test User',
        'email': 'test@example.com',
        'username': '$invalid_user'
    })
    assert b"Username is not valid." in response.data

    # signup without password
    response = test_client.post('/signup', data={
        'name': 'invalid Test User',
        'email': 'test@example.com',
        'username': 'testuser'
    })
    assert b"Password is required." in response.data

    # signup with password length less than 5
    response = test_client.post('/signup', data={
        'name': 'invalid Test User',
        'email': 'test@example.com',
        'password': '1234',
        'username': 'testuser'
    })
    assert b"Password length must be greater than 5 charactars" in response.data

    # signup without email
    response = test_client.post('/signup', data={
        'name': 'invalid Test User',
        'password': 'password',
        'username': 'testuser'
    })
    assert b"Email is not valid!!" in response.data

    # signup with correct credentials
    response = test_client.post('/signup', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'username': 'testuser'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == '/login'    

    # signup with same email
    response = test_client.post('/signup', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'username': 'testuser'
    })
    assert b"Email already registered!!" in response.data

    # signup with same user name
    response = test_client.post('/signup', data={
        'name': 'Test User',
        'email': 'test2@example.com',
        'password': 'password',
        'username': 'testuser'
    })
    assert b"Username already registered!!" in response.data

def test_login(test_client):
    # get login page
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data  

    # login without email
    response = test_client.post('/login', data={
        'password': 'password'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == '/login'

    # login without password
    response = test_client.post('/login', data={
        'email': 'test@example.com'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == '/login'

    # password length less than 6
    response = test_client.post('/login', data={
        'email': 'test@example.com',
        'password': '12345'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == '/login'

    # post login without registering
    response = test_client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == '/signup'

    # add user to database
    member = Member(username="testuser", email="test@example.com", password="password", admin=False, active=True)
    member.set_password("password")
    member.save()

    # login with incorrect password
    response = test_client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == '/login'

    # login with correct details
    response = test_client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 302  # Check for redirect
    assert response.location == "/member/testuser"

    # get login when already logged in
    with test_client.session_transaction() as session:
        session['user'] = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'admin': False,
        }
        session['logged_in'] = True
    response = test_client.get('/login')
    assert response.status_code == 302  # Check for redirect
    assert response.location == "/"  # Redirect to home