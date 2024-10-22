# Weather Monitoring System

A comprehensive real-time weather monitoring system that retrieves data from OpenWeatherMap API, processes it, and provides insights through rollups, aggregates, and visualizations. The system monitors weather conditions for major Indian metropolitan cities and provides alerts for extreme weather conditions.

## Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Processing](#data-processing)
- [Visualization Types](#visualization-types)
- [Testing](#testing)
- [Deployment](#deployment)
- [Design Choices](#design-choices)
- [Known Limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Functionality
- Real-time weather data retrieval from OpenWeatherMap API
- Configurable update intervals (default: 10 minutes)
- Temperature conversion (Kelvin to Celsius)
- Support for multiple Indian metropolitan cities:
  - Delhi
  - Mumbai
  - Chennai
  - Bangalore
  - Kolkata
  - Hyderabad

### Weather Parameters
- Basic Parameters:
  - Temperature (current, feels like)
  - Weather conditions
  - Timestamp
- Extended Parameters:
  - Humidity
  - Wind speed and direction
  - Atmospheric pressure
  - Visibility
  - Cloud cover
  - Precipitation (rain/snow)

### Data Processing
- Daily weather summaries
- Rolling aggregates:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition
- Persistent storage in SQLite database
- Historical data tracking

### Alerting System
- Configurable temperature thresholds
- Consecutive update monitoring
- Real-time alert generation
- Console notifications
- Weather condition alerts

### Visualization
- Daily weather summaries
- Historical trend analysis
- Temperature variation charts
- Weather condition distribution
- Wind and humidity patterns
- Forecast visualizations

### Bonus Features
- 5-day weather forecast
- Extended weather parameters
- Forecast summaries and visualization
- Comprehensive weather dashboard

## System Architecture

```
┌─────────────────┐        ┌──────────────┐        ┌────────────────┐
│  OpenWeatherMap │ ─────► │  API Client  │ ─────► │ Data Processor │
└─────────────────┘        └──────────────┘        └────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐        ┌──────────────┐        ┌────────────────┐
│  Visualizations │ ◄───── │   Database   │ ◄───── │ Weather Data   │
└─────────────────┘        └──────────────┘        └────────────────┘
        │                                                  │
        │                  ┌──────────────┐               │
        └─────────────────►│Alert System  │◄──────────────┘
                          └──────────────┘
```

## Prerequisites

- Python 3.7 or higher
- OpenWeatherMap API key
- Git (for version control)
- Docker (optional, for containerization)
- Sufficient disk space for data storage
- Internet connection for API access

## Installation

### Standard Installation

1. Clone the repository:
```bash
git clone https://github.com/Ekansh1131/weather-monitoring.git
cd weather-monitoring
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/macOS
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
echo "OPENWEATHERMAP_API_KEY=your_api_key_here" > .env
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t weather-monitoring .
```

2. Run the container:
```bash
docker run -e OPENWEATHERMAP_API_KEY=your_api_key_here weather-monitoring
```

## Configuration

### Configuration Parameters (config.py)
```python
UPDATE_INTERVAL = 300  # API update interval in seconds
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
TEMPERATURE_UNIT = 'celsius'
TEMPERATURE_THRESHOLD = 35  # Alert threshold in Celsius
CONSECUTIVE_UPDATES_THRESHOLD = 2  # Number of consecutive high readings for alert
```

### Database Configuration
- Default: SQLite database (weather_data.db)
- Tables:
  - daily_weather_summary
  - weather_alerts
  - forecast_data

## Usage

### Running the Application
```bash
python main.py
```

### Command Line Options
```bash
python main.py --interval 300  # Set update interval
python main.py --temp-unit F   # Use Fahrenheit
python main.py --debug        # Enable debug logging
```

### Monitoring Output
- Console displays current conditions
- Alerts shown for threshold breaches
- Visualizations saved in 'visualizations' directory

## Project Structure

```
weather-monitoring/
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── config.py
│   ├── data_processor.py
│   ├── database.py
│   ├── alerting.py
│   ├── visualization.py
│   └── forecast_visualizer.py
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_data_processor.py
│   └── test_alerting.py
├── visualizations/
│   ├── daily_summary/
│   ├── forecasts/
│   └── trends/
├── main.py
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

## Data Processing

### Weather Data Pipeline
1. API data retrieval
2. Data parsing and validation
3. Temperature conversion
4. Aggregation and summary generation
5. Database storage
6. Alert checking
7. Visualization generation

### Data Storage Format
```sql
CREATE TABLE daily_weather_summary (
    id INTEGER PRIMARY KEY,
    city TEXT,
    date DATE,
    avg_temp REAL,
    max_temp REAL,
    min_temp REAL,
    dominant_weather TEXT,
    -- Additional columns...
);
```

## Visualization Types

### Current Weather
- Temperature trends
- Weather condition distribution
- Wind and humidity patterns

### Forecasts
- 5-day temperature forecast
- Precipitation probability
- Wind speed and direction

### Historical Data
- Daily temperature summaries
- Weather pattern analysis
- Alert history

## Testing

### Running Tests
```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_api_client
```

### Test Coverage
- System setup verification
- API connection testing
- Data retrieval validation
- Temperature conversion accuracy
- Daily summary calculations
- Alert system functionality

## Deployment

### Local Deployment
1. Follow standard installation steps
2. Configure environment variables
3. Run the application

### Docker Deployment
1. Build Docker image
2. Configure environment variables
3. Run container
4. Map volumes for persistence (optional)

## Design Choices

### Architecture Decisions
- Modular component design for maintainability
- SQLite for simple deployment
- Pandas for efficient data processing
- Matplotlib/Seaborn for visualization flexibility

### Data Storage
- SQLite: Lightweight, portable, no separate server needed
- DataFrame: Efficient in-memory processing
- File-based visualization storage

### Error Handling
- Comprehensive exception catching
- Graceful degradation
- Detailed error logging
- Automatic recovery attempts

## Known Limitations

- Single-threaded execution
- Limited historical data storage
- Console-based alerts only
- Basic visualization interactivity
- No web interface

## Troubleshooting

### Common Issues
1. API Connection Errors
   - Verify API key
   - Check internet connection
   - Validate city names

2. Database Errors
   - Check write permissions
   - Verify database integrity
   - Clear corrupted database

3. Visualization Issues
   - Check directory permissions
   - Verify matplotlib installation
   - Clear visualization cache

### Error Resolution
```bash
# Reset database
rm weather_data.db
python main.py

# Clear visualizations
rm -rf visualizations/*
mkdir -p visualizations
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For more information or support, please create an issue in the GitHub repository.
