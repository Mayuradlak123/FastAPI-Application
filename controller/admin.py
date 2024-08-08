import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def check(condition, message=""):
    if not condition:
        raise AssertionError(message)

def createQuestion():
    try:
        response = client.post(
            "/admin/add-question",
            params={"admin_username": ADMIN_USERNAME, "question": "What is 2+2?", "answer": "4"},
            headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="}  # Base64 encoded "admin:password"
        )
        check(response.status_code == 200, "Failed to create question")
        check(response.json()["question"] == "What is 2+2?", "Question text mismatch")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")

def readQuestion():
    try:
        response = client.get("/admin/get-questions", headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
        check(response.status_code == 200, "Failed to read questions")
        check(isinstance(response.json(), list), "Response is not a list")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")

def updateQuestion():
    try:
        response = client.put(
            "/admin/update-question",
            params={"id": 1, "question": "What is 3+3?"},
            headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="}
        )
        check(response.status_code == 200, "Failed to update question")
        check(response.json()["question"] == "What is 3+3?", "Updated question text mismatch")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")

def deleteQuestion():
    try:
        response = client.delete("/admin/delete-question?id=1", headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQ="})
        check(response.status_code == 200, "Failed to delete question")
        check(response.json() == {"message": "Question deleted successfully"}, "Deletion message mismatch")
    except AssertionError as e:
        pytest.fail(f"Test failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during test: {e}")
