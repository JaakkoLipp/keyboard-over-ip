from fastapi.testclient import TestClient
from server import app  # Import your FastAPI app

# Create a TestClient for interacting with the app
client = TestClient(app)

def test_post_input():
    """
    Test the POST /input endpoint.
    """
    # Arrange
    payload = {"input": "Test message"}

    # Act
    response = client.post("/input", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": 200, "message": "Input stored successfully"}


def test_get_output_no_data():
    """
    Test the GET /output endpoint when no data has been sent.
    """
    # Act
    response = client.get("/output")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"status": 404, "message": "No input available"}


def test_get_output_with_data():
    """
    Test the GET /output endpoint after sending data.
    """
    # Arrange
    payload = {"input": "Another test message"}
    client.post("/input", json=payload)  # Send data first

    # Act
    response = client.get("/output")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"input": "Another test message"}


def test_root_endpoint():
    """
    Test the root (/) endpoint.
    """
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Keyboard-over-internet backend is running!"}
