FROM nvidia/cuda:12.5.1-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg python3-venv pip

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]