"""testing for backend of app"""

import pytest
import mongomock
from app import create_app

@pytest.fixture
def client(monkeypatch):
    """
    Create and yield flask app
    """
    # use mock db for testing
    monkeypatch.setattr('pymongo.MongoClient', mongomock.MongoClient)
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_user(client):
    """
    Create a user to test logged in routes
    """
    client.post(
        "/register", 
        data={
            "username": "testuser12",
            "password": "randompass2$",
            "confirm_password": "randompass2$",
      },
   )

    client.post(
        "/",
        data={
            "username": "testuser12",
            "password": "randompass2$",
        }
    )
    return client


def test_index(client):
    """
    Test index route of web page
    """
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Login" in html


def test_register(client):
    """
    Test register route of web page
    """
    response = client.get("/register")
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Register" in html


def test_login_wrong_password(client):
    """
    Test login with wrong password
    """
    client.post(
        "/register",
        data={
            "username": "testuser1234",
            "password": "Random2$2",
            "confirm_password": "Random2$2",
        },
    )
    client.get("/logout", follow_redirects=True)

    response = client.post(
        "/",
        data={
            "username": "testuser1234",
            "password": "wrongpassword",
        },
        follow_redirects=True,
    )

    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Incorrect Password" in html

def test_invalid_login(client):
    """
    Test login with invalid information
    """
    response = client.post(
        "/", data={"username": "testuser1234", "password": "randompassword1234"}
    )
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "User not found" in html


def test_home_page(mock_user):
    """
    Test home page when logged in
    """
    response = mock_user.get("/home")
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Recent Meals" in html


def test_add_meal_get(mock_user):
    """
    Test add meal page 
    """
    response = mock_user.get("/add-meal")
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Add a meal" in html


def test_add_meal_post(mock_user):
    """
    Test posting a new meal
    """
    response = mock_user.post(
        "/add-meal",
        data={
            "food_list": "banana apple",
            "meal_type": "Lunch",
            "date": "2025-04-28",
        },
        follow_redirects=True
    )
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Meal Summary" in html
    

def test_logout(mock_user):
    """
    Test logging user out
    """
    response = mock_user.get("/logout", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Login" in html