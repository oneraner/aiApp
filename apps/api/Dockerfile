FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Cloud Run uses PORT env variable (default 8080)
ENV PORT=8080

# Uvicorn with production settings
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers"]
