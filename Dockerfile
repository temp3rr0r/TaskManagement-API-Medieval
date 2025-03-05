FROM python:3.9-slim

WORKDIR /app

# Create data directory
RUN mkdir -p /app/data

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the PDF file to the container
COPY data/knowledge_base.pdf /app/data/

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 