import time
from datetime import date
from src.config import CITIES, UPDATE_INTERVAL
from src.api_client import OpenWeatherMapClient
from src.data_processor import WeatherDataProcessor
from src.database import DatabaseManager
from src.alerting import AlertSystem
from src.visualization import WeatherVisualizer
from src.forecast_visualizer import ForecastVisualizer

def process_current_weather(city, api_client, data_processor, db_manager, alert_system, visualizer):
    """Process current weather data for a city"""
    try:
        print(f"\nFetching current weather data for {city}...")
        raw_data = api_client.get_weather_data(city)
        weather_data = api_client.parse_weather_data(raw_data)
        
        # Display current conditions
        print(f"Current conditions in {city}:")
        print(f"  Temperature: {weather_data['temp']:.1f}°C")
        print(f"  Feels like: {weather_data['feels_like']:.1f}°C")
        print(f"  Weather: {weather_data['description']}")
        print(f"  Humidity: {weather_data['humidity']}%")
        print(f"  Wind: {weather_data['wind_speed']} m/s")
        
        # Process and store data
        try:
            data_processor.add_weather_data(weather_data)
            
            # Process daily summary
            today = date.today()
            daily_summary = data_processor.get_daily_summary(city, today)
            
            if daily_summary:
                try:
                    db_manager.save_daily_summary(city, daily_summary)
                    print(f"✓ Updated daily summary for {city}")
                except Exception as db_error:
                    print(f"Error saving summary to database for {city}: {str(db_error)}")
            else:
                print(f"Could not generate daily summary for {city}")

            # Check for alerts
            if alert_system.check_temperature_alert(city, weather_data['temp']):
                alert_system.generate_alert(city, weather_data['temp'])
                
        except Exception as process_error:
            print(f"Error processing data for {city}: {str(process_error)}")

        return True
    except Exception as e:
        print(f"Error fetching weather data for {city}: {str(e)}")
        return False

def process_forecast(city, api_client, data_processor, forecast_visualizer):
    """Process forecast data for a city"""
    try:
        print(f"\nFetching forecast data for {city}...")
        raw_forecast = api_client.get_forecast_data(city)
        forecast_data = api_client.parse_forecast_data(raw_forecast)
        
        # Store forecast data
        data_processor.add_forecast_data(city, forecast_data)
        
        # Generate forecast summaries
        forecast_summaries = data_processor.get_forecast_summary(city)
        
        # Check for weather alerts
        alerts = data_processor.get_weather_alerts(city)
        if alerts:
            print(f"\nWeather Alerts for {city}:")
            for alert in alerts:
                print(f"  ⚠️ {alert['type']}: {alert['description']}")
        
        # Generate forecast visualizations
        forecast_visualizer.plot_temperature_forecast(city, forecast_data)
        forecast_visualizer.plot_precipitation_forecast(city, forecast_data)
        forecast_visualizer.plot_wind_forecast(city, forecast_data)
        forecast_visualizer.create_forecast_dashboard(city, forecast_data)
        forecast_visualizer.plot_forecast_summary(city, forecast_summaries)
        
        print(f"✓ Generated forecast visualizations for {city}")
        return True
    except Exception as e:
        print(f"Error processing forecast for {city}: {str(e)}")
        return False

def main():
    print("\n=== Weather Monitoring System Starting ===\n")
    
    # Initialize components
    try:
        api_client = OpenWeatherMapClient()
        data_processor = WeatherDataProcessor()
        db_manager = DatabaseManager()
        alert_system = AlertSystem()
        visualizer = WeatherVisualizer()
        forecast_visualizer = ForecastVisualizer()
        print("✓ Successfully initialized all components")
    except Exception as e:
        print(f"ERROR initializing components: {str(e)}")
        return

    print(f"\nMonitoring weather for cities: {', '.join(CITIES)}")
    print(f"Update interval: {UPDATE_INTERVAL} seconds")
    print("\nPress Ctrl+C to stop the monitoring...\n")

    try:
        while True:
            for city in CITIES:
                # Process current weather
                process_current_weather(city, api_client, data_processor, 
                                     db_manager, alert_system, visualizer)
                
                # Process forecast (every hour)
                if int(time.time()) % 3600 < UPDATE_INTERVAL:
                    process_forecast(city, api_client, data_processor, 
                                  forecast_visualizer)

            # Generate current weather visualizations
            try:
                recent_data = data_processor.get_recent_data()
                if not recent_data.empty:
                    visualizer.plot_temperature_trends(recent_data)
                    visualizer.plot_weather_conditions(recent_data)

                    today = date.today()
                    summaries = db_manager.get_daily_summaries(
                        today.replace(day=1), 
                        today
                    )
                    if summaries:
                        visualizer.plot_daily_summary(summaries)
            except Exception as e:
                print(f"Error generating visualizations: {str(e)}")

            # Clean up old data
            data_processor.clear_old_data()

            print(f"\nSleeping for {UPDATE_INTERVAL} seconds...")
            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nStopping weather monitoring system...")
        print("Goodbye!")

if __name__ == "__main__":
    main()