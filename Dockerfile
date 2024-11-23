# Use the official Python 3.12 image as the base
FROM python:3.12.7-bookworm

# Set environment variables to ensure Python runs in an optimized way
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required system dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Override the environment variables
RUN export SECRET_KEY=$(python -c 'import os; print(os.urandom(24).hex())')

RUN echo "flask db upgrade && flask run --host=0.0.0.0 --port=3000" > /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run database migrations AND the application
CMD ["/usr/bin/bash", "/entrypoint.sh"]
