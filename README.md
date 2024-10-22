# Weather Monitoring System

A real-time weather monitoring system that retrieves data from OpenWeatherMap API and provides insights through rollups and aggregates.

## Features

- Real-time weather monitoring for Indian metros
- Daily weather summaries with aggregates
- Temperature and weather condition alerts
- Comprehensive visualizations
- 5-day weather forecasts
- Extended weather parameters (humidity, wind, pressure, etc.)

## Prerequisites

- Python 3.11
- OpenWeatherMap API key
- Docker (optional)

## Installation

### Standard Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-monitoring.git
cd weather-monitoring
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```
OPENWEATHERMAP_API_KEY=your_api_key_here
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

## Design Choices

1. Data Storage:
   - SQLite for simplicity and portability
   - Structured schema for daily summaries
   - In-memory DataFrame for real-time processing

2. Architecture:
   - Modular design with separate components
   - Event-driven processing
   - Configurable parameters

3. Visualization:
   - Matplotlib/Seaborn for static visualizations
   - Multiple visualization types for different insights
   - Automated file organization

4. Error Handling:
   - Comprehensive error catching
   - Graceful degradation
   - Detailed logging

## Running Tests

```bash
python -m unittest discover tests
```

## Future Improvements

1. Add email notifications for alerts
2. Implement a web interface
3. Add more sophisticated forecasting
4. Enhance visualization interactivity
5. Implement data backup mechanisms