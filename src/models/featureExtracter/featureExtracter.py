import os
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json


SYSTEM_INSTRUCTION = """
You are a helpful research assistant. You help social science scholars to search for papers more easily through sepcific datasets and variables.
Your job is to read throught the paper and tell the use which datasets are used in this paper and return some specific features for this paper.
These features will then be used to form a new seach platform for papers.
"""

# Setup for Google Cloud Project and Vertex AI Initialization
GCP_PROJECT = os.environ.get("ac215", "ac215-438315")
GCP_LOCATION = "us-central1"
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# Model for content generation
GENERATIVE_MODEL = "gemini-1.5-flash-001"
generative_model = GenerativeModel(
	GENERATIVE_MODEL,
	system_instruction=[SYSTEM_INSTRUCTION]
)

# Configuration settings for content generation
generation_config = GenerationConfig(
    max_output_tokens=2048,
    temperature=0.2,
    top_p=0.95,
    top_k=40
)


schema = {
    "dataset_information": [
        {
            "formal_name": "",
            "source_repository": "",
            "timeframe": "",
            "geographical_scope": "",
            "population_sample": "",
            "unit_of_analysis": "",
            "data_format": "",
            "sample_size": "",
            "missing_data": "",
            "data_collection_method": "",
            "data_cleaning": "",
            "usage_in_paper": {
                "variable_type": "",
                "specifics": ""
            }
        }
    ],
    "study_context": {
        "study_title": "",
        "authors": [
            {
                "name": "",
                "affiliations": [""]
            }
        ],
        "publication_year": "",
        "research_domain": ""
    },
    "variables": {
        "dependent_variables": [
            {
                "name": "",
                "type": "",
                "measurement": ""
            }
        ],
        "independent_variables": [
            {
                "name": "",
                "type": "",
                "categories": [""]
            }
        ],
        "control_variables": [
            {
                "name": "",
                "type": "",
                "measurement": ""
            }
        ]
    }
}

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

    
def extract_information(text):
    # Prepare the prompt for extracting information
    prompt = f"""
    Extract the following information from the given paper text according to this schema:
    {json.dumps(schema, indent=4)}

    Paper Text:
    {text}

    Provide the extracted information in JSON format.
    """

    # Generate the response using the model

    response = generative_model.generate_content(
		[prompt],  # Input prompt
		generation_config=generation_config,  # Configuration settings
		stream=False,  # Enable streaming for responses
	)

    generated_text = response.text

    return generated_text

def main():

    txt_path = '/Users/haozhuo/Documents/GSD_2024Fall/Advanced_Practical_Data_Science/Project/MS2/AC215-Paper-with-Data/src/models/featureExtracter/output.1.txt'  # Replace with your text file path
    text = read_text_file(txt_path)
    
    # Extract structured information from the full text
    extracted_info = extract_information(text)
    
    # Convert the extracted information to a dictionary and save it
    try:
        extracted_data = json.loads(extracted_info)
        with open("extracted_information.json", "w") as json_file:
            json.dump(extracted_data, json_file, indent=4)
        print(json.dumps(extracted_data, indent=4))
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Raw extracted info:", extracted_info)


if __name__ == '__main__':
    main()