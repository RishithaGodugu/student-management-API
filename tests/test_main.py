from fastapi.testclient import TestClient
from validation.main import app

client=TestClient(app)

def test_Welcome():
    response=client.get("/")

    assert response.status_code==200

    assert response.json()=={
        "message":"Welcome to Student Management API"
    }

def test_invalid_endpoint():
    response=client.get("/invalid-url")

    assert response.status_code==404

def test_invalid_student_data():
    response=client.post(
        "/students",
        json={}
    )

    assert response.status_code==422