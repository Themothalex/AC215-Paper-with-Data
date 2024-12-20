#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -ex

cd "$(dirname "$0")"

# Set vairables
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/
export GCP_PROJECT="ac215-438315" # CHANGE TO YOUR PROJECT ID
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"
export IMAGE_NAME="paper-with-data"


# Create the network if we don't have it yet
docker network inspect llm-rag-network >/dev/null 2>&1 || docker network create llm-rag-network

# # Build the image based on the Dockerfile
# docker build -t $IMAGE_NAME -f Dockerfile .

# Build images for each service based on their respective Dockerfiles
docker compose build

# # Run All Containers
# # docker compose run --rm --service-ports $IMAGE_NAME
docker compose up -d --remove-orphans

# # Build the image based on the Dockerfile
# docker build -t $IMAGE_NAME -f Dockerfile .

# # Run Container
# docker run --rm --name $IMAGE_NAME -ti \
# -v "$BASE_DIR":/app \
# -v "$SECRETS_DIR":/secrets \
# -v "$PERSISTENT_DIR":/persistent \
# -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
# -e GCP_PROJECT=$GCP_PROJECT \
# $IMAGE_NAME