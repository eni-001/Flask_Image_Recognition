"""Focused tests for the Flask application routes."""

from io import BytesIO
from unittest.mock import patch


def test_home_page_loads(client):
    """Confirm that the homepage loads and displays its main heading."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hand Sign Digit Language Detection" in response.data
    assert b"Choose file" in response.data


def test_prediction_route_rejects_get_request(client):
    """Confirm that the prediction route only accepts POST requests."""
    response = client.get("/prediction")

    assert response.status_code == 405


def test_prediction_without_file(client):
    """Confirm that submitting without a file displays an error."""
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data


def test_successful_prediction_displays_result(client):
    """Confirm that a valid processed upload displays its prediction."""
    with patch("app.preprocess_img", return_value="processed_image"):
        with patch("app.predict_result", return_value=7):
            response = client.post(
                "/prediction",
                data={"file": (BytesIO(b"image-data"), "digit.jpg")},
                content_type="multipart/form-data",
            )

    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b">7<" in response.data
    assert b"File cannot be processed." not in response.data
