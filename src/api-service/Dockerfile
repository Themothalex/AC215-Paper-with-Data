FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel pipenv

# Copy Pipfile and install Python dependencies
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pipenv install --deploy || pipenv install --system --ignore-pipfile

# Copy the rest of the source code
COPY . /app

# Expose the API port
EXPOSE 9000

# Set the entry point for the container
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
