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


def fetch_weather_data(city="London", units="metric", lang="en", cnt=None, output_file="raw_weather_data.json"):
    """
    Fetch weather data from the OpenWeatherMap API and save it to a file.

    Parameters:
        city (str): The name of the city to fetch data for. Default is "London".
        units (str): Units of measurement ("metric", "imperial", or "standard"). Default is "metric".
        lang (str): Language for weather descriptions (e.g., "en" for English). Default is "en".
        cnt (int): Number of timestamps to fetch. Optional.
        output_file (str): File path to save the API response. Default is 'raw_weather_data.json'.

    Returns:
        dict: The raw JSON response from the API.

    Raises:
        ValueError: If the API key is missing or an HTTP error occurs.

    Saves:
        The API response in a JSON file.
    """
    if not API_KEY:
        logging.error("API key not found. Ensure it is set in the .env file.")
        raise ValueError("API key not found. Please set it in the .env file.")
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": lang,
    }
    
    if cnt:
        params["cnt"] = cnt

    try:
        logging.info(f"Fetching weather data for city: {city} with parameters: {params}")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        logging.info(f"Received response: {len(data.get('list', []))} records fetched.")

        # Save the data to a file
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Weather data successfully saved to {output_file}")

        return data

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        raise
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
        raise


if __name__ == "__main__":
    # Example invocation
    fetch_weather_data(city="New York", units="metric", lang="en", cnt=50)
