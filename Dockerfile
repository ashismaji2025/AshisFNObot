# Use official Python 3.10 image
FROM python:3.10-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Copy files
COPY . /app/

# Install pip packages
RUN pip install --upgrade pip
RUN pip install "python-telegram-bot[webhooks]==20.6"

# Expose the bot port
EXPOSE 10000

# Start the bot
CMD ["python", "main.py"]
