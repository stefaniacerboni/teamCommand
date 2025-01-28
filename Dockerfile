FROM python:3.9-slim

# Install system dependencies for Chrome + Chromedriver
RUN apt-get update && apt-get install -y wget unzip gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome (or Chromium) + Chromedriver
# For example, installing Chromium might look like:
RUN apt-get update && apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your code
COPY . /app
WORKDIR /app

# Expose the port
EXPOSE 8080

# Start command
CMD gunicorn app:app --bind 0.0.0.0:8080 --timeout 120

