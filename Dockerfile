# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update apt-get and install necessary libraries for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for Python to not buffer output (useful for logs)
ENV PYTHONUNBUFFERED=1

# Install pip and Python dependencies
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Make sure the virtual environment's Python is used for the app
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the app (assumes uvicorn is installed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
