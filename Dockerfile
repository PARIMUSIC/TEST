FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure audio file exists (optional: you can mount it at runtime)
# COPY audio.mp3 ./audio.mp3

CMD ["python", "main.py"]
