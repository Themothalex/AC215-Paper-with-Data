import os
import argparse
import pandas as pd
import json
import time
import glob
from google.cloud import storage
import vertexai
from vertexai.preview.tuning import sft
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
TRAIN_DATASET = "gs://fine-tuning-ac215/train_data.jsonl"
VALIDATION_DATASET = "gs://fine-tuning-ac215/validation_data.jsonl"
GCP_LOCATION = "us-central1"
GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002"  # gemini-1.5-pro-002
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)


def train(wait_for_job=False):
    print("train()")

    # Supervised Fine Tuning
    sft_tuning_job = sft.train(
        source_model=GENERATIVE_SOURCE_MODEL,
        train_dataset=TRAIN_DATASET,
        # validation_dataset=VALIDATION_DATASET,
        epochs=1,  # change to 2-3
        adapter_size=4,
        learning_rate_multiplier=1.0,
        # tuned_model_display_name="-cheese-demo-v1",
        tuned_model_display_name="datawithpaper-demo-v1",
    )
    print("Training job started. Monitoring progress...\n\n")

    # Wait and refresh
    time.sleep(60)
    sft_tuning_job.refresh()

    if wait_for_job:
        print("Check status of tuning job:")
        print(sft_tuning_job)
        while not sft_tuning_job.has_ended:
            time.sleep(60)
            sft_tuning_job.refresh()
            print("Job in progress...")

    print(f"Tuned model name: {sft_tuning_job.tuned_model_name}")
    print(
        f"Tuned model endpoint name: {sft_tuning_job.tuned_model_endpoint_name}"
    )
    print(f"Experiment: {sft_tuning_job.experiment}")


def process():
    # print("chat()")
    # Get the model endpoint from Vertex AI: https://console.cloud.google.com/vertex-ai/studio/tuning?project=ac215-project
    MODEL_ENDPOINT = "projects/590232342668/locations/us-central1/endpoints/7908374821732352000"
    generative_model = GenerativeModel(MODEL_ENDPOINT)

    # check if the model works and test the performance
    with open("demo_paper.txt", "r", encoding="utf-8") as f:
        query = f.read()

    prompt = """
    Provide the extracted information in **strict JSON format** without any additional text or explanation.

Here is the JSON file you need to fill:

{
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
Here is the paper from which you should extract information:

    """

    response = generative_model.generate_content(
        [prompt + query],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
    )
    generated_text = response.text
    print("Fine-tuned LLM Response:", generated_text)


def main(args=None):
    print("CLI Arguments:", args)

    if args.train:
        train()

    if args.process:
        process()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--train",
        action="store_true",
        help="Train model",
    )
    parser.add_argument(
        "--process",
        action="store_true",
        help="Chat with model",
    )

    args = parser.parse_args()

    main(args)
