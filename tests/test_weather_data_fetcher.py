import pytest
from weather_data_fetcher import fetch_weather_data
from unittest.mock import patch
import logging
import os
import json

@pytest.fixture
def mock_response():
    return {
        "list": [
            {
                "dt": 1700000000,
                "main": {
                    "temp": 20.0,
                    "humidity": 50,
                    "pressure": 1012
                }
            },
        ]
    }

@patch("weather_data_fetcher.API_KEY", "mock_api_key")
def test_fetch_weather_data(mocker, mock_response, caplog, tmp_path):
    # Mock the requests.get call to return a mock response
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Temporary file for testing
    temp_file = tmp_path / "test_weather_data.json"

    # Capture logs during the function call
    with caplog.at_level(logging.INFO):
        data = fetch_weather_data(city="MockCity", output_file=str(temp_file))

    # Verify that requests.get was called with correct parameters
    mock_get.assert_called_once_with(
        "http://api.openweathermap.org/data/2.5/forecast",
        params={
            "q": "MockCity",
            "appid": "mock_api_key",
            "units": "metric",
            "lang": "en",
        },
    )

    # Validate the returned data
    assert data == mock_response, "Returned data does not match the mock response"

    # Check if log messages are recorded
    assert "Fetching weather data for city: MockCity" in caplog.text
    assert f"Weather data successfully saved to {temp_file}" in caplog.text

    # Verify the output file was created
    assert os.path.exists(temp_file), f"{temp_file} not created"

    # Validate the content of the output file
    with open(temp_file, "r") as f:
        saved_data = json.load(f)
    assert saved_data == mock_response, "Saved data does not match the mock response"
