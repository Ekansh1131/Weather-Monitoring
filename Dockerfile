# Use Python 3.11 as base image
FROM python:3.11.3

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cacheK
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create visualizations directory
RUN mkdir -p visualizations

# Environment variables
ENV OPENWEATHERMAP_API_KEY=your_api_key_here
ENV UPDATE_INTERVAL=300
ENV TEMPERATURE_UNIT=celsius

# Run the application
CMD ["python", "main.py"]