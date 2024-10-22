from src.api_client import OpenWeatherMapClient
from src.config import CITIES

def test_api_connection():
    print("Testing API connection...")
    
    try:
        client = OpenWeatherMapClient()
        
        for city in CITIES:
            print(f"\nTesting weather data retrieval for {city}:")
            data = client.get_weather_data(city)
            parsed_data = client.parse_weather_data(data)
            
            print(f"✓ Successfully retrieved data:")
            print(f"  - Temperature: {parsed_data['temp']:.1f}°C")
            print(f"  - Feels like: {parsed_data['feels_like']:.1f}°C")
            print(f"  - Weather: {parsed_data['main']}")
        
        print("\n✓ All API tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error during API testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_api_connection()