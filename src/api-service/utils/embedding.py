import json
import numpy as np
from vertexai.language_models import TextEmbeddingModel
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model
EMBEDDING_MODEL = "text-embedding-004"
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

def extract_features_from_json(json_file):
    text_blocks = []
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
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
            text_representation = extract_features_from_json(json_data)
            embedding = generate_embedding(text_representation)
            json_embeddings.append({"path": json_file_path, "embedding": embedding})
    return json_embeddings

def find_best_match(input_text, json_embeddings):
    input_embedding = generate_embedding(input_text)
    best_score = -1
    best_match = None
    for json_embedding in json_embeddings:
        similarity = cosine_similarity([input_embedding], [json_embedding["embedding"]])[0][0]
        if similarity > best_score:
            best_score = similarity
            best_match = json_embedding
    return best_match, best_score
