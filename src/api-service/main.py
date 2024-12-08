from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import os
import json
import vertexai
from vertexai.language_models import TextEmbeddingModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Setup Google Cloud Project and Vertex AI Initialization
GCP_PROJECT = os.environ.get("ac215", "ac215-438315")
GCP_LOCATION = "us-central1"
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# Load the embedding model
EMBEDDING_MODEL = "text-embedding-004"
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Backend API",
    description="A Retrieval-Augmented Generation (RAG) API for querying relevant documents based on Independent and Dependent variables.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Metadata", "description": "API for fetching metadata information."},
        {"name": "Search", "description": "API for searching documents and retrieving best matches."},
    ]
)

# Define API model
class QueryRequest(BaseModel):
    independent_variable: str = None
    dependent_variable: str = None
    region: str = None
    data_unit: str = None

@app.get("/", tags=["Metadata"])
async def root():
    """
    Get API Index
    """
    return {"message": "Welcome to the RAG Backend API!"}

@app.get("/metadata", tags=["Metadata"])
async def get_metadata():
    """
    Fetch metadata about the available datasets, such as variable types and general information.
    """
    metadata = {
        "available_variables": ["independent_variable", "dependent_variable", "region", "data_unit"],
        "description": "This API helps in searching documents related to various study variables."
    }
    return metadata

@app.post("/search", tags=["Search"])
async def search(query: QueryRequest):
    """
    Search for relevant documents based on the input variables.
    """
    try:
        # Combine all input fields to create a query
        input_text_parts = []
        if query.independent_variable:
            input_text_parts.append(f"Independent Variable: {query.independent_variable}")
        if query.dependent_variable:
            input_text_parts.append(f"Dependent Variable: {query.dependent_variable}")
        if query.region:
            input_text_parts.append(f"Region: {query.region}")
        if query.data_unit:
            input_text_parts.append(f"Data Unit: {query.data_unit}")

        # If no input fields are provided, raise an error
        if not input_text_parts:
            raise HTTPException(status_code=400, detail="At least one input field must be provided.")

        input_text = "; ".join(input_text_parts)
        print(f"Input text for RAGProcessor: {input_text}")

        # Set paths to JSON files
        # json_files = [
        #     "data/feature_1.json",
        #     "data/feature_2.json",
        #     "data/feature_3.json"
        # ]

        # Generate embeddings for JSON files
        json_embeddings = generate_embeddings_for_json_files(json_files)
        print(f"Generated embeddings for JSON files: {json_files}")

        # Find best matching JSON files
        matches = find_all_matches(input_text, json_embeddings, query)
        print(f"Found matches: {matches}")

        if not matches:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        # Return sorted matches
        return {
            "results": [
                {
                    "similarity_score": match["similarity_score"],
                    "study_title": match["study_title"],
                    "authors": match["authors"],
                    "publication_year": match["publication_year"],
                    "summary": match["summary"]
                }
                for match in matches[:5]
            ]
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility functions
def extract_features_from_json(json_file, variable_type=None):
    text_blocks = []
    if variable_type == "independent_variable":
        text_blocks.append(json.dumps(json_file["variables"].get("independent_variables", []), indent=2))
    elif variable_type == "dependent_variable":
        text_blocks.append(json.dumps(json_file["variables"].get("dependent_variables", []), indent=2))
    else:
        text_blocks.append(json.dumps(json_file["dataset_information"], indent=2))
        text_blocks.append(json.dumps(json_file["study_context"], indent=2))
        text_blocks.append(json.dumps(json_file["variables"], indent=2))
    return " ".join(text_blocks)

def generate_embedding(text):
    embedding_input = [text]
    embeddings = embedding_model.get_embeddings(embedding_input)
    return np.array(embeddings[0].values)

def generate_embeddings_for_json_files(json_file_paths):
    json_embeddings = []

    for json_file_path in json_file_paths:
        try:
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
                json_embeddings.append({
                    "path": json_file_path,
                    "independent_variable_embedding": generate_embedding(extract_features_from_json(json_data, "independent_variable")),
                    "dependent_variable_embedding": generate_embedding(extract_features_from_json(json_data, "dependent_variable")),
                    "study_title": json_data["study_context"].get("study_title", ""),
                    "authors": [author["name"] for author in json_data["study_context"].get("authors", [])],
                    "publication_year": json_data["study_context"].get("publication_year", ""),
                    "summary": json.dumps(json_data["dataset_information"], indent=2)
                })
        except Exception as e:
            print(f"Error processing file {json_file_path}: {e}")

    return json_embeddings

def find_all_matches(input_text, json_embeddings, query):
    matches = []
    
    if query.independent_variable:
        input_embedding = generate_embedding(query.independent_variable)
        for json_embedding in json_embeddings:
            try:
                similarity = cosine_similarity([input_embedding], [json_embedding["independent_variable_embedding"]])[0][0]
                matches.append({
                    "similarity_score": similarity,
                    "study_title": json_embedding["study_title"],
                    "authors": json_embedding["authors"],
                    "publication_year": json_embedding["publication_year"],
                    "summary": json_embedding["summary"]
                })
            except Exception as e:
                print(f"Error calculating similarity for file {json_embedding['path']}: {e}")

    if query.dependent_variable:
        input_embedding = generate_embedding(query.dependent_variable)
        for json_embedding in json_embeddings:
            try:
                similarity = cosine_similarity([input_embedding], [json_embedding["dependent_variable_embedding"]])[0][0]
                matches.append({
                    "similarity_score": similarity,
                    "study_title": json_embedding["study_title"],
                    "authors": json_embedding["authors"],
                    "publication_year": json_embedding["publication_year"],
                    "summary": json_embedding["summary"]
                })
            except Exception as e:
                print(f"Error calculating similarity for file {json_embedding['path']}: {e}")

    # Sort matches by similarity score in descending order
    matches = sorted(matches, key=lambda x: x["similarity_score"], reverse=True)

    return matches
