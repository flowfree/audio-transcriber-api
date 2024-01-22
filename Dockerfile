# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN apt update && \
    apt install -y ffmpeg &&  \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI code to the container
COPY . .
