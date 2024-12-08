#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="api"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json"

echo $SECRETS_DIR
echo $GOOGLE_APPLICATION_CREDENTIALS

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
        -v "$BASE_DIR":/app \
        -v "$SECRETS_DIR":/secrets \
        -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json" \
        -p 9000:9000 \
        $IMAGE_NAME
