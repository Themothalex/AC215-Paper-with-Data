#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

export IMAGE_NAME="gemini-finetuner"

# Define some environment variables
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
export GCP_PROJECT="ac215-438315" # CHANGE TO YOUR PROJECT ID
export GCS_BUCKET_NAME="cheese-dataset" # CHANGE TO YOUR PROJECT BUCKET
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"
export GCP_SERVICE_ACCOUNT="llm-service-account@ac215-438315.iam.gserviceaccount.com" # CHANGE TO YOUR PROJECT ID
export LOCATION="us-central1"



# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
$IMAGE_NAME
