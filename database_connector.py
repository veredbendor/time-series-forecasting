from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_weather_data(records):
    """
    Inserts weather data into the Supabase table.
    """
    try:
        print("Inserting records:", records)  # Log the records being inserted
        response = supabase.table("weather_data").insert(records).execute()
        print("Response:", response)
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise

