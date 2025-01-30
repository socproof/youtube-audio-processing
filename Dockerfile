FROM nvidia/cuda:12.5.1-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg python3-venv pip

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application
COPY . /app
