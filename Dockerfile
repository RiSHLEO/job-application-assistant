# Base image — official Python 3.11 on a lightweight Linux
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer
# If requirements haven't changed, Docker skips reinstalling
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./backend/

# Copy the .env file if it exists
COPY .env* ./

# Expose port 8000
EXPOSE 8000

# Command to run when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]