# Use official Python 3.10 image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ Force install PTB webhooks extra manually
RUN pip install "python-telegram-bot[webhooks]==20.6"

# Expose the port Flask or webhook server will use
EXPOSE 10000

# Run the bot
CMD ["python", "main.py"]
