import pytest
import requests
from weather_data_fetcher import fetch_weather_data
from unittest.mock import patch
import os
import json
import logging

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
def test_fetch_weather_data(mocker, mock_response, caplog):
    # Mock the requests.get call to return a mock response
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Capture logs during the function call
    with caplog.at_level(logging.INFO):
        fetch_weather_data(city="MockCity")

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

    # Check if log messages are recorded
    assert "Weather data fetched and saved to raw_weather_data.json" in caplog.text

    # Verify the output file was created
    assert os.path.exists("raw_weather_data.json"), "raw_weather_data.json file not created"

    # Validate the content of the output file
    with open("raw_weather_data.json", "r") as f:
        saved_data = json.load(f)
    assert "list" in saved_data, "Key 'list' not found in the saved data"
    assert saved_data["list"] == mock_response["list"], "Saved data does not match the mock response"

    # Validate specific fields in the saved data
    assert saved_data["list"][0]["main"]["temp"] == 20.0, "Temperature value is incorrect"
    assert saved_data["list"][0]["main"]["humidity"] == 50, "Humidity value is incorrect"
    assert saved_data["list"][0]["main"]["pressure"] == 1012, "Pressure value is incorrect"
