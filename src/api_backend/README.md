# Backend API for Retrieval-Augmented Generation (RAG)

## Overview

This project is a backend API built using **FastAPI** for a Retrieval-Augmented Generation (RAG) system. The API integrates with **Google Cloud's Vertex AI** to provide similarity-based search and natural language generation capabilities. It allows users to input independent or dependent variables, along with other details, and returns the most relevant documents, ranked by similarity.

## Features

- **Search API**: Users can input search terms such as independent variables, dependent variables, region, or data unit to find related documents.
- **Similarity Search**: The system uses **cosine similarity** between the user's input and document embeddings to rank the relevance of documents.
- **Google Cloud Integration**: Uses **Vertex AI** to generate embeddings for textual data.

## Folder Structure

```
backend-api/
  |- data/
      |- feature_1.json
      |- feature_2.json
      |- feature_3.json
  |- main.py
  |- requirements.txt
  |- README.md
  |- utils/
      |- embedding.py
  |- rag_connector.py
```

### Key Files

- **`main.py`**: The primary FastAPI application for serving the backend API.
- **`rag_connector.py`**: Implements the logic to connect with the RAG model for processing queries.
- **`utils/embedding.py`**: Contains utility functions for generating text embeddings.
- **`data/`**: Directory containing JSON files that represent the document data used for search.

## Setup Instructions

### Prerequisites

- **Python 3.9** or later.
- **Google Cloud SDK**: Required for authentication with Google Cloud services.
- **Docker** (optional): If you wish to run the API inside a Docker container.

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd backend-api
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Google Cloud Credentials**:
   - Make sure to authenticate with Google Cloud by running:
     ```bash
     gcloud auth login
     ```
   - Set the environment variable for Google Application Credentials:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
     ```

### Running the API

1. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 9000
   ```
2. **Access the API Documentation**:
   - The API documentation is available at [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs).

### Testing the API

- **Using `curl` Command**:
  ```bash
  curl -X POST "http://127.0.0.1:9000/search" \
  -H "Content-Type: application/json" \
  -d '{"independent_variable": "Household Composition", "dependent_variable": "Residential Segregation"}'
  ```

- **Using Postman**:
  1. Install **Postman** and create a new **POST** request.
  2. Set the request URL to `http://127.0.0.1:9000/search`.
  3. Add the required body parameters in JSON format (e.g., `{"independent_variable": "Household Composition"}`).
  4. Click **Send** to test the API.

## How It Works

1. **Input Variables**: Users can specify independent variables, dependent variables, region, or data unit.
2. **Embedding Generation**: The API uses Google Vertex AI's text embedding model to generate vector embeddings for the user query and the document data.
3. **Similarity Matching**: The cosine similarity between the input query and document embeddings is calculated to find the most relevant documents.
4. **Response**: The matched documents are returned in descending order of similarity.

## Environment Variables

- `GCP_PROJECT`: The Google Cloud project ID.
- `GCP_LOCATION`: The location for the Vertex AI resources.
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to the Google Cloud service account credentials.

## Deployment

### Docker Deployment

1. **Build the Docker Image**:
   ```bash
   docker build -t backend-api .
   ```
2. **Run the Docker Container**:
   ```bash
   docker run -p 9000:9000 backend-api


