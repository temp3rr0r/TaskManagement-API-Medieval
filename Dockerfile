FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including pandoc
RUN apt-get update && apt-get install -y \
    pandoc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create data directory
RUN mkdir -p /app/data

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the data directory containing PDF and EPUB files
COPY data/ /app/data/

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 