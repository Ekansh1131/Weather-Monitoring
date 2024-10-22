import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from .config import VISUALIZATION_OUTPUT_DIR

class ForecastVisualizer:
    def __init__(self):
        os.makedirs(os.path.join(VISUALIZATION_OUTPUT_DIR, 'forecasts'), exist_ok=True)
        plt.style.use('seaborn-v0_8')
        sns.set_theme()

    def plot_temperature_forecast(self, city, forecast_data):
        df = pd.DataFrame(forecast_data)
        df['date_time'] = pd.to_datetime(df['date_time'])
        
        plt.figure(figsize=(15, 6))
        plt.plot(df['date_time'], df['temp'], 'b-', label='Temperature')
        plt.plot(df['date_time'], df['feels_like'], 'r--', label='Feels Like')
        plt.fill_between(df['date_time'], df['temp_min'], df['temp_max'], alpha=0.2)
        
        plt.title(f'Temperature Forecast for {city}')
        plt.xlabel('Date/Time')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'forecasts', f'{city}_temp_forecast.png')
        plt.savefig(filepath)
        plt.close()

    def plot_precipitation_forecast(self, city, forecast_data):
        df = pd.DataFrame(forecast_data)
        df['date_time'] = pd.to_datetime(df['date_time'])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
        
        # Precipitation probability
        ax1.plot(df['date_time'], df['pop'] * 100, 'b-')
        ax1.set_ylabel('Precipitation Probability (%)')
        ax1.set_title(f'Precipitation Forecast for {city}')
        ax1.grid(True)
        
        # Rain and snow amounts
        ax2.bar(df['date_time'], df['rain_3h'], label='Rain', alpha=0.6)
        ax2.bar(df['date_time'], df['snow_3h'], label='Snow', alpha=0.6)
        ax2.set_xlabel('Date/Time')
        ax2.set_ylabel('Precipitation (mm/3h)')
        ax2.legend()
        ax2.grid(True)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'forecasts', f'{city}_precip_forecast.png')
        plt.savefig(filepath)
        plt.close()

    def plot_wind_forecast(self, city, forecast_data):
        df = pd.DataFrame(forecast_data)
        df['date_time'] = pd.to_datetime(df['date_time'])
        
        fig, ax = plt.subplots(figsize=(15, 6))
        
        # Wind speed
        ax.plot(df['date_time'], df['wind_speed'], 'g-', label='Wind Speed')
        ax.set_xlabel('Date/Time')
        ax.set_ylabel('Wind Speed (m/s)')
        ax.set_title(f'Wind Forecast for {city}')
        
        # Wind direction arrows
        for i in range(0, len(df), 4):  # Plot arrow every 4 points to avoid crowding
            angle = df['wind_direction'].iloc[i]
            speed = df['wind_speed'].iloc[i]
            dx = -np.cos(np.radians(angle)) * speed / 5
            dy = -np.sin(np.radians(angle)) * speed / 5
            ax.arrow(df['date_time'].iloc[i], speed, dx, dy, 
                    head_width=0.5, head_length=0.8, fc='g', ec='g', alpha=0.5)
        
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'forecasts', f'{city}_wind_forecast.png')
        plt.savefig(filepath)
        plt.close()

    def create_forecast_dashboard(self, city, forecast_data):
        """Create a comprehensive forecast dashboard"""
        df = pd.DataFrame(forecast_data)
        df['date_time'] = pd.to_datetime(df['date_time'])
        
        fig = plt.figure(figsize=(15, 12))
        gs = fig.add_gridspec(3, 2)
        
        # Temperature plot
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(df['date_time'], df['temp'], 'b-', label='Temperature')
        ax1.plot(df['date_time'], df['feels_like'], 'r--', label='Feels Like')
        ax1.fill_between(df['date_time'], df['temp_min'], df['temp_max'], alpha=0.2)
        ax1.set_title('Temperature Forecast')
        ax1.set_ylabel('Temperature (°C)')
        ax1.legend()
        ax1.grid(True)
        
        # Precipitation plot
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.bar(df['date_time'], df['rain_3h'], label='Rain', alpha=0.6)
        ax2.bar(df['date_time'], df['snow_3h'], label='Snow', alpha=0.6)
        ax2.set_title('Precipitation Forecast')
        ax2.set_ylabel('Amount (mm/3h)')
        ax2.legend()
        ax2.grid(True)
        
        # Humidity and Clouds plot
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(df['date_time'], df['humidity'], 'b-', label='Humidity')
        ax3.plot(df['date_time'], df['clouds'], 'g--', label='Cloud Cover')
        ax3.set_title('Humidity and Cloud Cover')
        ax3.set_ylabel('Percentage (%)')
        ax3.legend()
        ax3.grid(True)
        
        # Wind plot
        ax4 = fig.add_subplot(gs[2, :])
        ax4.plot(df['date_time'], df['wind_speed'], 'g-', label='Wind Speed')
        ax4.set_title('Wind Speed Forecast')
        ax4.set_xlabel('Date/Time')
        ax4.set_ylabel('Speed (m/s)')
        ax4.legend()
        ax4.grid(True)
        
        # Adjust layout and save
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'forecasts', f'{city}_forecast_dashboard.png')
        plt.savefig(filepath)
        plt.close()

    def plot_forecast_summary(self, city, forecast_summaries):
        """Plot daily forecast summaries"""
        df = pd.DataFrame(forecast_summaries)
        df['date'] = pd.to_datetime(df['date'])
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Temperature summary
        ax1.plot(df['date'], df['avg_temp'], 'b-', label='Average')
        ax1.plot(df['date'], df['max_temp'], 'r--', label='Max')
        ax1.plot(df['date'], df['min_temp'], 'g--', label='Min')
        ax1.set_title('Temperature Forecast')
        ax1.set_ylabel('Temperature (°C)')
        ax1.legend()
        ax1.grid(True)
        
        # Humidity
        ax2.plot(df['date'], df['avg_humidity'], 'b-')
        ax2.set_title('Average Humidity')
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True)
        
        # Precipitation
        ax3.bar(df['date'], df['total_rain'], label='Rain', alpha=0.6)
        ax3.bar(df['date'], df['total_snow'], label='Snow', alpha=0.6)
        ax3.set_title('Daily Precipitation')
        ax3.set_ylabel('Amount (mm)')
        ax3.legend()
        ax3.grid(True)
        
        # Wind speed
        ax4.plot(df['date'], df['avg_wind_speed'], 'g-')
        ax4.set_title('Average Wind Speed')
        ax4.set_ylabel('Speed (m/s)')
        ax4.grid(True)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'forecasts', f'{city}_forecast_summary.png')
        plt.savefig(filepath)
        plt.close()