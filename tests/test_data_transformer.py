import pytest
from data_transformer import transform_weather_data, transform_and_store_weather_data
from unittest.mock import patch
import json
import pandas as pd

@pytest.fixture
def mock_raw_file(tmp_path, mock_response):
    raw_file = tmp_path / "raw_weather_data.json"
    with open(raw_file, "w") as f:
        json.dump(mock_response, f)
    return raw_file

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

def test_transform_weather_data(mock_raw_file):
    # Call the transformation function
    df = transform_weather_data(raw_file=mock_raw_file)

    # Assert the DataFrame is not empty
    assert not df.empty, "DataFrame is empty"

    # Assert the columns match the expected schema
    expected_columns = {"timestamp", "temperature", "humidity", "pressure"}
    assert set(df.columns) == expected_columns, "Unexpected columns in DataFrame"

    # Validate the content of the DataFrame
    assert df.iloc[0]["temperature"] == 20.0, "Temperature value is incorrect"
    assert df.iloc[0]["humidity"] == 50, "Humidity value is incorrect"
    assert df.iloc[0]["pressure"] == 1012, "Pressure value is incorrect"
    assert pd.Timestamp("2023-11-14 22:13:20") == df.iloc[0]["timestamp"], "Timestamp value is incorrect"

@patch("data_transformer.insert_weather_data")
def test_transform_and_store_weather_data(mock_insert, mock_raw_file):
    # Call the transformation and storage function
    transform_and_store_weather_data(raw_file=mock_raw_file, city="TestCity")

    # Validate the mock insert function was called
    mock_insert.assert_called_once()

    # Validate the data passed to the insert function
    inserted_data = mock_insert.call_args[0][0]
    assert inserted_data[0]["city"] == "TestCity", "City value is incorrect"
    assert inserted_data[0]["temperature"] == 20.0, "Temperature value is incorrect"
    assert inserted_data[0]["humidity"] == 50, "Humidity value is incorrect"
    assert inserted_data[0]["pressure"] == 1012, "Pressure value is incorrect"
    assert inserted_data[0]["timestamp"] == pd.Timestamp("2023-11-14 22:13:20"), "Timestamp value is incorrect"
