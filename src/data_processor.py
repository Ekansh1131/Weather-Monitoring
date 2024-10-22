import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .config import TEMPERATURE_UNIT

class WeatherDataProcessor:
    def __init__(self):
        self.current_data = {}
        self.forecast_data = {}
        
    def add_weather_data(self, weather_data):
        """Add new weather data for a city"""
        try:
            city = weather_data['city']
            if city not in self.current_data:
                self.current_data[city] = pd.DataFrame()
            
            # Create a copy of the data to avoid modifying the original
            data_copy = weather_data.copy()
            
            # Handle special weather conditions
            if isinstance(data_copy.get('main'), str):
                data_copy['main'] = data_copy['main'].strip()
            
            # Convert to DataFrame and add date
            df = pd.DataFrame([data_copy])
            df['date'] = pd.to_datetime(df['dt'], unit='s').dt.date
            
            # Ensure all numeric columns have valid values
            numeric_columns = ['temp', 'feels_like', 'humidity', 'pressure', 
                             'wind_speed', 'clouds', 'visibility', 'rain_1h', 'snow_1h']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Concatenate with existing data
            self.current_data[city] = pd.concat([self.current_data[city], df], 
                                              ignore_index=True)
            print(f"Successfully added weather data for {city}")
            
        except Exception as e:
            print(f"Error adding weather data for {city}: {str(e)}")
            raise

    def get_daily_summary(self, city, date):
        """Get daily summary for a specific city and date"""
        if city not in self.current_data:
            print(f"No data available for {city}")
            return None
            
        daily_data = self.current_data[city][self.current_data[city]['date'] == date]
        if daily_data.empty:
            print(f"No data available for {city} on {date}")
            return None

        try:
            # Calculate dominant weather condition
            weather_mode = daily_data['main'].mode()
            dominant_weather = weather_mode.iloc[0] if not weather_mode.empty else 'Unknown'
            
            # Calculate detailed description
            desc_mode = daily_data['description'].mode()
            detailed_description = desc_mode.iloc[0] if not desc_mode.empty else 'Unknown'
            
            summary = {
                'date': date,
                'avg_temp': float(daily_data['temp'].mean()),
                'max_temp': float(daily_data['temp'].max()),
                'min_temp': float(daily_data['temp'].min()),
                'dominant_weather': dominant_weather,
                'detailed_description': detailed_description,
                'avg_humidity': float(daily_data['humidity'].mean()),
                'avg_pressure': float(daily_data['pressure'].mean()),
                'avg_wind_speed': float(daily_data['wind_speed'].mean()),
                'max_wind_speed': float(daily_data['wind_speed'].max()),
                'dominant_wind_direction': self._get_dominant_wind_direction(daily_data['wind_direction']),
                'total_rain': float(daily_data.get('rain_1h', pd.Series([0])).sum()),
                'total_snow': float(daily_data.get('snow_1h', pd.Series([0])).sum()),
                'avg_clouds': float(daily_data['clouds'].mean()),
                'avg_visibility': float(daily_data['visibility'].mean())
            }
            
            print(f"Generated summary for {city} on {date}")
            return summary
            
        except Exception as e:
            print(f"Error creating summary for {city}: {str(e)}")
            print(f"Data for {city}:")
            print(daily_data)
            return None
        
    def get_forecast_summary(self, city):
        """Get forecast summary for a city"""
        if city not in self.forecast_data:
            return None
            
        df = self.forecast_data[city]
        if df.empty:
            return None
            
        try:
            # Group by date for daily summaries
            daily_groups = df.groupby('date')
            
            summaries = []
            for date, group in daily_groups:
                summary = {
                    'date': date,
                    'avg_temp': group['temp'].mean(),
                    'max_temp': group['temp'].max(),
                    'min_temp': group['temp'].min(),
                    'dominant_weather': group['main'].mode().iloc[0],
                    'avg_humidity': group['humidity'].mean(),
                    'avg_wind_speed': group['wind_speed'].mean(),
                    'precipitation_probability': group.get('pop', pd.Series([0])).max(),
                    'total_rain': group.get('rain_3h', pd.Series([0])).sum(),
                    'total_snow': group.get('snow_3h', pd.Series([0])).sum()
                }
                summaries.append(summary)
                
            return summaries
            
        except Exception as e:
            print(f"Error creating forecast summary for {city}: {str(e)}")
            return None

    def get_weather_alerts(self, city):
        """Get weather alerts based on forecast data"""
        if city not in self.forecast_data or self.forecast_data[city].empty:
            return []
            
        alerts = []
        forecast = self.forecast_data[city]
        
        try:
            # High temperature alert
            high_temp_periods = forecast[forecast['temp'] > 35]
            if not high_temp_periods.empty:
                dates = high_temp_periods['datetime'].dt.date.unique()
                alerts.append({
                    'type': 'High Temperature',
                    'description': f"Temperatures above 35°C expected on {', '.join(str(d) for d in dates)}"
                })
            
            # Heavy rain alert
            heavy_rain_periods = forecast[forecast['rain_3h'] > 10]
            if not heavy_rain_periods.empty:
                dates = heavy_rain_periods['datetime'].dt.date.unique()
                alerts.append({
                    'type': 'Heavy Rain',
                    'description': f"Heavy rain expected on {', '.join(str(d) for d in dates)}"
                })
            
            # Strong wind alert
            strong_wind_periods = forecast[forecast['wind_speed'] > 20]
            if not strong_wind_periods.empty:
                dates = strong_wind_periods['datetime'].dt.date.unique()
                alerts.append({
                    'type': 'Strong Winds',
                    'description': f"Strong winds expected on {', '.join(str(d) for d in dates)}"
                })
            
        except Exception as e:
            print(f"Error generating weather alerts for {city}: {str(e)}")
        
        return alerts

    def get_recent_data(self, hours=24):
        """Get recent data for all cities"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = []
        
        for city, df in self.current_data.items():
            if not df.empty:
                recent = df[df['dt'] > cutoff_time.timestamp()].copy()
                if not recent.empty:
                    recent_data.append(recent)
        
        if not recent_data:
            return pd.DataFrame()
        
        return pd.concat(recent_data, ignore_index=True)

    def _get_dominant_wind_direction(self, wind_degrees):
        """Convert wind degrees to cardinal directions"""
        try:
            directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                         'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            
            # Convert degrees to 16-point compass direction
            val = int((wind_degrees.mean() / 22.5) + 0.5)
            return directions[val % 16]
        except Exception as e:
            print(f"Error calculating wind direction: {str(e)}")
            return 'N'

    def clear_old_data(self, days=7):
        """Remove data older than specified days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        for city in self.current_data:
            if not self.current_data[city].empty:
                self.current_data[city] = self.current_data[city][
                    self.current_data[city]['dt'] > cutoff_time.timestamp()
                ]