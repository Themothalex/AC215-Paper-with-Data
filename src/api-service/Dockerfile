FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Pipfile and install Python dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --deploy

# Copy the rest of the source code
COPY . /app

# Expose the API port
EXPOSE 9000

# Set the entry point for the container
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]

