import pytest
from fastapi.testclient import TestClient
from app.main import app

# Initialize the TestClient with the FastAPI app
client = TestClient(app)

def check(condition, message=""):
    if not condition:
        raise AssertionError(message)

@pytest.fixture
def CreateUser():
    try:
        # Fixture to create a test user
        response = client.post("/user/create-user", params={"username": "testuser", "password": "testpass"})
        check(response.status_code == 200, "Failed to create test user")
        return response.json()
    except AssertionError as e:
        pytest.fail(f"Setup failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during setup: {e}")

def CreateTest(create_test_user):
    try:
        # Test to create a new user
        user = create_test_user
        check(user["username"] == "testuser", "Username does not match")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")

def AttemptTest(create_test_user):
    try:
        # Test to take a test
        response = client.get("/user/attempt-test", params={"username": "testuser"})
        check(response.status_code == 200, "Failed to attempt test")
        check(isinstance(response.json(), list), "Response is not a list")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")

def SubmitTest(create_test_user):
    try:
        # Test to submit an answer
        response = client.post("/user/submit-test", params={
            "username": "testuser",
            "question_id": 1,
            "answer": "4"
        })
        check(response.status_code == 200, "Failed to submit answer")
        check(response.json() == {"message": "Answer submitted successfully"}, "Response message mismatch")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")

def getScore(create_test_user):
    try:
        # Test to get the score
        response = client.get("/user/get-score", params={"username": "testuser"})
        check(response.status_code == 200, "Failed to get score")
        check(isinstance(response.json(), int), "Score is not an integer")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")
