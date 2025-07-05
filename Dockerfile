# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Copy project
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install "python-telegram-bot[webhooks]==20.6"

# Expose port
EXPOSE 10000

# Run the bot
CMD ["python", "main.py"]
