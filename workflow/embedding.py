import os
import json
import vertexai
from vertexai.language_models import TextEmbeddingModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Setup Google Cloud Project and Vertex AI Initialization
GCP_PROJECT = os.environ.get("ac215", "ac215-438315")
GCP_LOCATION = "us-central1"
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# Load the embedding model
EMBEDDING_MODEL = "text-embedding-004"
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

def extract_features_from_json(json_file):
    # Extract dataset information, study context, and variables into a text block
    text_blocks = []
    
    # Convert the JSON into a single string representation
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
        # print(json_file_path)
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
            text_representation = extract_features_from_json(json_data)
            embedding = generate_embedding(text_representation)
            json_embeddings.append({"path": json_file_path, "embedding": embedding})

    return json_embeddings

def find_best_match(input_text, json_embeddings):
    # Generate embedding for the input text
    input_embedding = generate_embedding(input_text)

    # Calculate similarity scores
    best_score = -1
    best_match = None

    for json_embedding in json_embeddings:
        similarity = cosine_similarity([input_embedding], [json_embedding["embedding"]])[0][0]
        if similarity > best_score:
            best_score = similarity
            best_match = json_embedding

    return best_match, best_score

def main():
    # Set paths to your JSON files
    json_files = [
        "data/embedding/feature_1.json",
        "data/embedding/feature_2.json",
        "data/embedding/feature_3.json"
        # Add paths to other JSON files here
    ]

    # Input variables to match
    input_text = "Household Type, including Male Same-Sex Households, Female Same-Sex Households, and Different-Sex Households."

    # Generate embeddings for JSON files
    json_embeddings = generate_embeddings_for_json_files(json_files)

    # Find the best matching JSON file based on the input text
    best_match, best_score = find_best_match(input_text, json_embeddings)

    if best_match:
        print(f"Best match: {best_match['path']}")
        print(f"Similarity score: {best_score}")
    else:
        print("No match found.")

if __name__ == "__main__":
    main()