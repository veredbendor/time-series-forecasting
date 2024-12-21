# Time-Series Forecasting Project

This project focuses on building a time-series forecasting system with machine learning-based anomaly detection, including automated data collection, transformation, and scheduling.

---

## Weather Data Fetcher

The `weather_data_fetcher.py` module fetches weather data from the OpenWeatherMap API and saves the response to a file.

### Features
- Fetches weather forecast data for a specified city.
- Supports metric, imperial, and standard units.
- Saves the response in a JSON file for further processing.
- Logs detailed information about the fetch operation.

---

### Setup

1. **Environment Setup**:
   - Install required dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Add your OpenWeatherMap API key to a `.env` file:
     ```plaintext
     OPENWEATHERMAP_API_KEY=your_api_key_here
     ```

2. **Run in Docker**:
   - Build and run the container:
     ```bash
     docker-compose up --build
     ```
   - Fetch weather data:
     ```bash
     docker-compose run --rm app python weather_data_fetcher.py
     ```

3. **Manual Run**:
   - Run the script directly (outside Docker):
     ```bash
     python weather_data_fetcher.py
     ```

---

### Usage

#### Function: `fetch_weather_data`

Fetch weather data from the OpenWeatherMap API and save it to a file.

**Parameters**:
- `city` (str): The name of the city (default: `"London"`).
- `units` (str): Units of measurement:
  - `"metric"` (default) for Celsius.
  - `"imperial"` for Fahrenheit.
  - `"standard"` for Kelvin.
- `lang` (str): Language for weather descriptions (default: `"en"`).
- `cnt` (int): Number of timestamps to fetch (optional).
- `output_file` (str): File path to save the API response (default: `"raw_weather_data.json"`).

**Returns**:
- `dict`: The raw JSON response from the API.

**Example**:
```python
from weather_data_fetcher import fetch_weather_data

data = fetch_weather_data(city="New York", units="metric", lang="en", cnt=5)
print(data)
