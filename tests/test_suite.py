import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, date
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import OpenWeatherMapClient
from src.data_processor import WeatherDataProcessor
from src.database import DatabaseManager
from src.alerting import AlertSystem

class TestWeatherSystem(unittest.TestCase):
    def setUp(self):
        self.api_client = OpenWeatherMapClient()
        self.data_processor = WeatherDataProcessor()
        self.db_manager = DatabaseManager()
        self.alert_system = AlertSystem()

    def test_api_connection(self):
        """Test 1: System Setup - API Connection"""
        try:
            data = self.api_client.get_weather_data("Delhi")
            self.assertIsNotNone(data)
            self.assertIn('main', data)
            self.assertIn('temp', data['main'])
            print("✓ API connection test passed")
        except Exception as e:
            self.fail(f"API connection failed: {str(e)}")

    def test_data_retrieval(self):
        """Test 2: Data Retrieval"""
        city = "Delhi"
        data = self.api_client.get_weather_data(city)
        parsed_data = self.api_client.parse_weather_data(data)
        
        required_fields = ['city', 'temp', 'feels_like', 'main', 'dt']
        for field in required_fields:
            self.assertIn(field, parsed_data)
            
        self.assertEqual(parsed_data['city'], city)
        print("✓ Data retrieval test passed")

    @patch('src.api_client.OpenWeatherMapClient.get_weather_data')
    def test_temperature_conversion(self, mock_get_weather):
        """Test 3: Temperature Conversion"""
        # Mock API response
        mock_get_weather.return_value = {
            'name': 'Delhi',
            'main': {'temp': 300.15, 'feels_like': 305.15},  # Kelvin values
            'weather': [{'main': 'Clear'}],
            'dt': int(datetime.now().timestamp())
        }
        
        data = self.api_client.get_weather_data("Delhi")
        parsed_data = self.api_client.parse_weather_data(data)
        
        # Verify conversion (300.15K = 27°C)
        self.assertAlmostEqual(parsed_data['temp'], 27, delta=1)
        print("✓ Temperature conversion test passed")

    def test_daily_summary(self):
        """Test 4: Daily Weather Summary"""
        # Simulate weather updates
        test_data = {
            'city': 'TestCity',
            'temp': 25.0,
            'feels_like': 26.0,
            'main': 'Clear',
            'description': 'clear sky',
            'humidity': 60,
            'pressure': 1013,
            'wind_speed': 5.0,
            'wind_direction': 180,
            'clouds': 20,
            'visibility': 10000,
            'rain_1h': 0,
            'snow_1h': 0,
            'dt': int(datetime.now().timestamp())
        }
        
        self.data_processor.add_weather_data(test_data)
        summary = self.data_processor.get_daily_summary('TestCity', date.today())
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['avg_temp'], 25.0)
        self.assertEqual(summary['dominant_weather'], 'Clear')
        print("✓ Daily summary test passed")

    def test_alerting_system(self):
        """Test 5: Alerting Thresholds"""
        # Test normal temperature
        self.alert_system.check_temperature_alert('TestCity', 30)
        self.assertEqual(self.alert_system.consecutive_high_temp_count.get('TestCity', 0), 0)
        
        # Test threshold breach
        self.alert_system.check_temperature_alert('TestCity', 36)
        self.alert_system.check_temperature_alert('TestCity', 36)
        self.assertEqual(self.alert_system.consecutive_high_temp_count['TestCity'], 2)
        
        # Verify alert is generated
        alert_message = self.alert_system.generate_alert('TestCity', 36)
        self.assertIsNotNone(alert_message)
        print("✓ Alerting system test passed")

def run_tests():
    """Run all tests and print results"""
    print("\nRunning Weather Monitoring System Tests...")
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests()