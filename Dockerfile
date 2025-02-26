# Use a small Python base image
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Copy requirement file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your code
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run uvicorn with that port declare by Cloud Run
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

