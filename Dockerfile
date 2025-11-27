# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required by PyTgCalls for audio handling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Audio file (optional: you can also mount it at runtime)
# COPY audio.mp3 .  # Uncomment if you want to bake it into the image

# Run the bot
CMD ["python", "main.py"]
