FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg is required by pytgcalls)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your audio file and main script
COPY audio.mp3 .
COPY main.py .

# Set environment variables (you'll override these at runtime)
ENV API_ID=123456
ENV API_HASH=your_api_hash
ENV SESSION_STRING=your_session_string
ENV AUDIO_FILE=audio.mp3
ENV DEFAULT_VOLUME=100

CMD ["python", "main.py"]
