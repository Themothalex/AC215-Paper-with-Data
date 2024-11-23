import os
import json
import vertexai
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, GenerationConfig
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Setup Google Cloud Project and Vertex AI Initialization
GCP_PROJECT = os.environ.get("ac215", "ac215-438315")
GCP_LOCATION = "us-central1"
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# Load the embedding model
EMBEDDING_MODEL = "text-embedding-004"
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}


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
        "data/feature_1.json",
        "data/feature_2.json",
        "data/feature_3.json"
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

    MODEL_ENDPOINT = "projects/590232342668/locations/us-central1/endpoints/7908374821732352000" 
    generative_model = GenerativeModel(MODEL_ENDPOINT)

    if best_match:
        with open(best_match['path'], "r") as f:
            text_summary = f.read()

        prompt_1 = f"""The user is interested in {input_text}. 
        
        Here is the summary of the most relevant paper.\n"""

        prompt_2 = text_summary

        prompt_3 = """

        Please tell the user how the paper is related to the query.

        You should first provide the basic information of the paper and then tell how they are related and finally convert the JSON file into a list of points.
            
            """
        
        prompt = prompt_1 + prompt_2 + prompt_3
        
        response = generative_model.generate_content(
        [prompt],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
        )

        generated_text = response.text
        print("Fine-tuned LLM Response:", generated_text)

if __name__ == "__main__":
    main()
