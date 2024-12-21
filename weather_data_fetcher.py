import requests
import json
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_weather_data(city="London", units="metric", lang="en", cnt=None):
    """
    Fetch weather data from the OpenWeatherMap API and save it to a file.

    Parameters:
        city (str): The name of the city to fetch data for. Default is "London".
        units (str): Units of measurement ("metric", "imperial", or "standard"). Default is "metric".
        lang (str): Language for weather descriptions (e.g., "en" for English). Default is "en".
        cnt (int): Number of timestamps to fetch. Optional.

    Raises:
        ValueError: If the API key is missing or an HTTP error occurs.

    Saves:
        A file named "raw_weather_data.json" containing the API response.
    """
    if not API_KEY:
        logging.error("API key not found.")
        raise ValueError("API key not found. Please set it in the .env file.")
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": lang,
    }
    
    # Add optional parameters
    if cnt:
        params["cnt"] = cnt

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        with open("raw_weather_data.json", "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Weather data fetched and saved to raw_weather_data.json")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        raise

if __name__ == "__main__":
    # Example invocation
    fetch_weather_data(city="New York", units="metric", lang="en", cnt=5)
