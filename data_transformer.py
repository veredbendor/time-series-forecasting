import json
import pandas as pd
import logging
from database_connector import insert_weather_data  # Ensure this exists

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transform_weather_data(raw_file="raw_weather_data.json"):
    """
    Transforms raw weather data into a structured pandas DataFrame.

    Parameters:
        raw_file (str): Path to the raw JSON file. Default is 'raw_weather_data.json'.

    Returns:
        pd.DataFrame: A DataFrame containing transformed weather data.
    """
    try:
        # Load raw JSON data
        logging.info(f"Loading raw weather data from {raw_file}")
        with open(raw_file, "r") as f:
            raw_data = json.load(f)
        
        # Extract relevant fields
        records = [
            {
                "timestamp": pd.to_datetime(entry["dt"], unit="s"),
                "temperature": entry["main"]["temp"],
                "humidity": entry["main"]["humidity"],
                "pressure": entry["main"]["pressure"],
            }
            for entry in raw_data["list"]
        ]
        
        # Create a pandas DataFrame
        df = pd.DataFrame(records)
        logging.info("Successfully transformed raw weather data into a DataFrame")
        return df

    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        raise

def transform_and_store_weather_data(raw_file="raw_weather_data.json", city="Unknown"):
    """
    Transforms raw weather data and stores it in the database.

    Parameters:
        raw_file (str): Path to the raw JSON file. Default is 'raw_weather_data.json'.
        city (str): City name associated with the weather data.
    """
    try:
        # Transform data
        df = transform_weather_data(raw_file)

        # Add the city column to the DataFrame
        df["city"] = city

        # Convert the timestamp column to ISO 8601 string format
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Convert DataFrame to a list of dictionaries
        records = df.to_dict(orient="records")

        # Insert data into the database
        insert_weather_data(records)
        logging.info(f"Weather data for {city} successfully transformed and stored in the database.")
    except Exception as e:
        logging.error(f"Error transforming and storing data: {e}")
        raise
