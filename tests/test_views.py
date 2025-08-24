import mongomock
import pytest
from flask_mongoengine import MongoEngine
from mongoengine import disconnect

from app import app
from app.models import Book, Member


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # update db config
    app.config["MONGODB_SETTINGS"] = {
        "db": "mydatabase",
        "host": "mongodb://localhost",
        "mongo_client_class": mongomock.MongoClient,
        "uuidRepresentation": "standard",
    }

    disconnect()
    db = MongoEngine(app)
    yield
    disconnect()


@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client


def test_home_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"LMS for managing Books, Members, Transaction.." in response.data


def test_books_route(test_client):
    Book(bookID="1", title="Book 1", authors="Author 1").save()
    Book(bookID="2", title="Book 2", authors="Author 2").save()

    response = test_client.get("/books")
    assert response.status_code == 200
    assert b"Book 1" in response.data
    assert b"Book 2" in response.data


def test_logout(test_client):
    # without login
    response = test_client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    # with login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "testuser",
            "email": "test@example.com",
            "admin": False,
        }
        session["logged_in"] = True
    response = test_client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_dashboard_route(test_client):
    # without login
    response = test_client.get("/dashboard/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    # with login
    # simulate by creating a user session
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "testuser",
            "email": "test@example.com",
            "admin": False,
        }
        session["logged_in"] = True
    response = test_client.get("/dashboard/")
    assert response.status_code == 200
    assert b"Alias possimus" in response.data


def test_add_book_route(test_client):
    # without admin login
    response = test_client.get("/add-book")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    # with admin login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "testuser",
            "email": "test@example.com",
            "admin": True,
        }
        session["logged_in"] = True
    response = test_client.get("/add-book")
    assert response.status_code == 200
    assert b"Add Book" in response.data

    # try adding a book
    response = test_client.post(
        "/add-book",
        data={
            "title": "New Book",
            "authors": "New Author",
            "isbn": "1234567890",
            "publisher": "New Publisher",
            "page": "100",
        },
    )
    # app.logger.info("Add book response data: %s", response.data)
    assert response.status_code == 200
    assert b"Author" in response.data


def test_get_books(test_client):
    response = test_client.get("/books")
    assert response.status_code == 200
    assert b"BOOKS" in response.data


def test_fetch_members(test_client):
    # without admin login
    response = test_client.get("/members")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    # with admin login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "testuser",
            "email": "test@example.com",
            "admin": True,
        }
        session["logged_in"] = True
    response = test_client.get("/members")
    assert response.status_code == 200
    assert b"Members" in response.data


def test_get_member_details(test_client):
    # add member in test database
    member = Member(
        username="testuser",
        email="testuser@example.com",
        password="password",
        admin=False,
        active=True,
    )
    member.set_password("password")
    member.save()

    # login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "testuser",
            "email": "testuser@example.com",
            "admin": False,
        }
        session["logged_in"] = True

    response = test_client.get("/member/testuser")
    app.logger.info("Response data: %s", response.headers)
    assert response.status_code == 200
    assert b"testuser" in response.data


def test_update_member(test_client):
    # add member in test database
    member = Member(
        username="testuser",
        email="testuser@example.com",
        password="password",
        admin=False,
        active=False,
    )
    member.set_password("password")
    member.save()
    # admin login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "adminuser",
            "email": "adminuser@example.com",
            "admin": True,
        }
        session["logged_in"] = True
    member_id = member.id

    response = test_client.post(
        f"/member/{member_id}",
        data={
            "name": "My Name",
            "email": "testuser@example.com",
            "balance": 100,
            "active": True,
        },
    )
    app.logger.info("Response data: %s", response.headers)
    assert response.status_code == 302
    assert response.headers["Location"] == "testuser"


def test_get_transactions(test_client):
    # without login
    response = test_client.get("/transactions")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    # with  non admin login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "testuser",
            "email": "testuser@example.com",
            "admin": False,
        }
        session["logged_in"] = True
    response = test_client.get("/transactions")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    # with admin login
    with test_client.session_transaction() as session:
        session["user"] = {
            "username": "adminuser",
            "email": "adminuser@example.com",
            "admin": True,
        }
        session["logged_in"] = True
    response = test_client.get("/transactions")
    assert response.status_code == 200
    assert b"Transactions" in response.data


def test_404_page(test_client):
    response = test_client.get("/non-existent-page")
    assert response.status_code == 404
    assert b"404 Not Found" in response.data
