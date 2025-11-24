# Use Debian slim (works well on Railway)
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# System deps for ffmpeg & building extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    build-essential \
    libffi-dev \
    libssl-dev \
    pkg-config \
    libopus-dev \
    libsndfile1 \
 && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt /app/requirements.txt
COPY . /app

# Upgrade pip then install python deps
RUN python -m pip install --upgrade pip setuptools wheel
# Install pytgcalls from github (dev branch) which is intended for Linux servers
RUN python -m pip install -r /app/requirements.txt

# Expose nothing (bot is outgoing). Set env and run main.
CMD ["python", "main.py"]
