import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from .config import VISUALIZATION_OUTPUT_DIR

class WeatherVisualizer:
    def __init__(self):
        os.makedirs(VISUALIZATION_OUTPUT_DIR, exist_ok=True)
        plt.style.use('seaborn-v0_8')
        sns.set_theme()

    def plot_temperature_trends(self, data):
        """Plot temperature trends for all cities"""
        if data.empty:
            return
            
        plt.figure(figsize=(15, 8))
        
        # Convert timestamp to datetime for better plotting
        data['datetime'] = pd.to_datetime(data['dt'], unit='s')
        
        # Plot each city's temperature
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            plt.plot(city_data['datetime'], city_data['temp'], 
                    marker='o', linestyle='-', label=city)
        
        plt.title('Temperature Trends by City')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'temperature_trends.png')
        plt.savefig(filepath)
        plt.close()

    def plot_weather_conditions(self, data):
        """Plot distribution of weather conditions"""
        if data.empty:
            return
            
        plt.figure(figsize=(12, 6))
        
        # Count occurrences of each weather condition
        condition_counts = data['main'].value_counts()
        
        # Create bar plot
        sns.barplot(x=condition_counts.index, y=condition_counts.values)
        plt.title('Weather Conditions Distribution')
        plt.xlabel('Weather Condition')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'weather_conditions.png')
        plt.savefig(filepath)
        plt.close()

    def plot_daily_summary(self, summaries):
        """Plot daily weather summaries"""
        if not summaries:
            return
        
        # Convert SQLAlchemy objects to DataFrame
        df = pd.DataFrame([{
            'date': s.date,
            'city': s.city,
            'avg_temp': s.avg_temp,
            'max_temp': s.max_temp,
            'min_temp': s.min_temp,
            'dominant_weather': s.dominant_weather
        } for s in summaries])
        
        # Create figure with multiple subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # Temperature trends
        for city in df['city'].unique():
            city_data = df[df['city'] == city]
            ax1.plot(city_data['date'], city_data['avg_temp'], 
                    marker='o', linestyle='-', label=f'{city} (Avg)')
            ax1.fill_between(city_data['date'], 
                           city_data['min_temp'], 
                           city_data['max_temp'], 
                           alpha=0.2)
        
        ax1.set_title('Daily Temperature Summary')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Temperature (°C)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)
        
        # Weather condition distribution
        condition_counts = df.groupby(['city', 'dominant_weather']).size().unstack(fill_value=0)
        condition_counts.plot(kind='bar', ax=ax2)
        ax2.set_title('Dominant Weather Conditions by City')
        ax2.set_xlabel('City')
        ax2.set_ylabel('Count')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'daily_summary.png')
        plt.savefig(filepath)
        plt.close()

    def plot_humidity_wind(self, data):
        """Plot humidity and wind speed trends"""
        if data.empty:
            return
            
        data['datetime'] = pd.to_datetime(data['dt'], unit='s')
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # Humidity trends
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            ax1.plot(city_data['datetime'], city_data['humidity'], 
                    marker='o', linestyle='-', label=city)
        
        ax1.set_title('Humidity Trends by City')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Humidity (%)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)
        
        # Wind speed trends
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            ax2.plot(city_data['datetime'], city_data['wind_speed'], 
                    marker='o', linestyle='-', label=city)
        
        ax2.set_title('Wind Speed Trends by City')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Wind Speed (m/s)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'humidity_wind.png')
        plt.savefig(filepath)
        plt.close()

    def plot_weather_dashboard(self, data):
        """Create a comprehensive weather dashboard"""
        if data.empty:
            return
            
        data['datetime'] = pd.to_datetime(data['dt'], unit='s')
        
        fig = plt.figure(figsize=(20, 15))
        gs = fig.add_gridspec(3, 2)
        
        # Temperature plot
        ax1 = fig.add_subplot(gs[0, :])
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            ax1.plot(city_data['datetime'], city_data['temp'], 
                    marker='o', linestyle='-', label=city)
        ax1.set_title('Temperature Trends')
        ax1.set_ylabel('Temperature (°C)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True)
        
        # Humidity plot
        ax2 = fig.add_subplot(gs[1, 0])
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            ax2.plot(city_data['datetime'], city_data['humidity'], 
                    marker='o', linestyle='-', label=city)
        ax2.set_title('Humidity Trends')
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True)
        
        # Wind speed plot
        ax3 = fig.add_subplot(gs[1, 1])
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            ax3.plot(city_data['datetime'], city_data['wind_speed'], 
                    marker='o', linestyle='-', label=city)
        ax3.set_title('Wind Speed Trends')
        ax3.set_ylabel('Wind Speed (m/s)')
        ax3.grid(True)
        
        # Weather conditions distribution
        ax4 = fig.add_subplot(gs[2, :])
        condition_counts = data.groupby(['city', 'main']).size().unstack(fill_value=0)
        condition_counts.plot(kind='bar', ax=ax4)
        ax4.set_title('Weather Conditions Distribution')
        ax4.set_xlabel('City')
        ax4.set_ylabel('Count')
        
        plt.tight_layout()
        filepath = os.path.join(VISUALIZATION_OUTPUT_DIR, 'weather_dashboard.png')
        plt.savefig(filepath)
        plt.close()