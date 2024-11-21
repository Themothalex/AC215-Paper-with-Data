import os
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
from google.cloud import storage

SYSTEM_INSTRUCTION = """
You are a helpful research assistant. You help social science scholars to search for papers more easily through specific datasets and variables.
Your job is to read through the paper and tell the user which datasets are used in this paper and return some specific features for this paper.
These features will then be used to form a new search platform for papers.
"""

# Setup for Google Cloud Project and Vertex AI Initialization
GCP_PROJECT = os.environ.get("ac215", "ac215-438315")
GCP_LOCATION = "us-east1"
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# Model for content generation
GENERATIVE_MODEL = "gemini-1.5-flash-001"
generative_model = GenerativeModel(
    "projects/590232342668/locations/us-central1/endpoints/7908374821732352000",
    system_instruction=[SYSTEM_INSTRUCTION]
)

# Configuration settings for content generation
generation_config = GenerationConfig(
    max_output_tokens=2048,
    temperature=0.2,
    top_p=0.95,
    top_k=40
)

# JSON schema for data extraction 

schema = {
    # (schema details here)
}

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def extract_information(text):
    prompt = f"""
{SYSTEM_INSTRUCTION}

Extract the following information from the given paper text according to this schema:
{json.dumps(schema, indent=4)}

Paper Text:
{text}

Provide the extracted information in **strict JSON format** without any additional text or explanation.
"""

    response = generative_model.generate_content(
        [prompt],
        generation_config=generation_config,
        stream=False,
    )
    return response.text.strip()

def upload_json_to_gcs(bucket_name, content, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Check if the blob already exists in the bucket
    if blob.exists():
        print(f"{destination_blob_name} already exists in gs://{bucket_name}/{destination_blob_name}. Skipping upload.")
        return

    # Save content to a local JSON file and upload
    with open("extracted_information.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)
    
    with open("extracted_information.json", "r", encoding="utf-8") as f:
        blob.upload_from_file(f, content_type="application/json")
    
    print(f"Uploaded {destination_blob_name} to gs://{bucket_name}/{destination_blob_name}")

def main():
    txt_path = 'data/ps8.txt'
    text = read_text_file(txt_path)
    
    # Extract structured information from the full text
    extracted_info = extract_information(text)

    # Debugging: Print extracted_info to inspect its contents
    # print("Extracted Information:", extracted_info)  # Inspect the raw output

    # Clean the extracted information to ensure it’s valid JSON
    extracted_info = extracted_info.strip()  # Remove extra whitespace
    if extracted_info.startswith("```json"):
        extracted_info = extracted_info[7:]  # Remove the ```json part
    if extracted_info.endswith("```"):
        extracted_info = extracted_info[:-3]  # Remove the ending ```

    try:
        extracted_data = json.loads(extracted_info)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print("Extracted Information content was not valid JSON.")
        return

    # Upload to GCS bucket
    output_bucket_name = "features_output"
    destination_blob_name = "extracted_information.json"
    # upload_json_to_gcs(output_bucket_name, extracted_data, destination_blob_name)

if __name__ == '__main__':
    main()
