FROM python:3.11-slim

WORKDIR /app

# Install git and build tools (needed by some Python packages)
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY . .

# Run the bot
CMD ["python3", "main.py"]
