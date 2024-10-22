import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OpenWeatherMap API key not found in .env file")

# General Configuration
UPDATE_INTERVAL = 300  # 5 minutes in seconds
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Hyderabad']
TEMPERATURE_UNIT = 'celsius'
DATABASE_URL = 'sqlite:///weather_data.db'

# Alerting Configuration
TEMPERATURE_THRESHOLD = 35
CONSECUTIVE_UPDATES_THRESHOLD = 2

# Visualization Configuration
VISUALIZATION_OUTPUT_DIR = 'visualizations'
os.makedirs(VISUALIZATION_OUTPUT_DIR, exist_ok=True)