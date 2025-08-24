import mongomock
import pytest
from flask_mongoengine import MongoEngine
from mongoengine import disconnect

from app import app
from app.models import Book, Member, Transaction

# @pytest.fixture(scope="function", autouse=True)
# def setup_db():
#     # update db config
#     app.config['MONGODB_SETTINGS'] = {
#         'db': 'mydatabase',
#         'host': 'mongodb://localhost',
#         'mongo_client_class': mongomock.MongoClient,
#         'uuidRepresentation': 'standard'
#     }

#     disconnect()
#     db = MongoEngine(app)
#     yield
#     disconnect()


@pytest.fixture(scope="function", autouse=True)
def test_app():
    # update app config for testing
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        MONGODB_SETTINGS={
            "db": "mydatabase",
            "host": "mongodb://localhost",
            "mongo_client_class": mongomock.MongoClient,
            "uuidRepresentation": "standard",
        },
    )

    disconnect()
    MongoEngine(app)
    yield
    disconnect()


def test_create_member():
    member = Member(
        name="testuser",
        email="test@example.com",
        password="password",
        username="testuser",
        admin=False,
        active=False,
    )
    assert member.username == "testuser"
    assert member.email == "test@example.com"
    assert not member.admin
    assert not member.active
    member.set_password("password")
    assert member.check_password("password")
    assert not member.is_admin()


def test_create_book():
    book = Book(
        bookID="1",
        title="Test Book",
        authors=["Author 1"],
        average_rating=4.5,
        isbn="1234567890123",
        isbn13="9781234567890",
        language_code="en",
        num_pages=300,
        ratings_count=100,
        text_reviews_count=10,
        publication_date="2023-01-01",
        publisher="Test Publisher",
    )
    assert book.title == "Test Book"
    assert book.authors == ["Author 1"]
    assert book.publication_date == "2023-01-01"
    assert book.isbn == "1234567890123"


def test_create_transaction():
    transaction = Transaction(
        id="1", member="1", book="1", borrow=True, date="2023-01-01"
    )
    assert transaction.id == "1"
    assert transaction.book == "1"
    assert transaction.member == "1"
    assert transaction.date == "2023-01-01"
    assert transaction.borrow
