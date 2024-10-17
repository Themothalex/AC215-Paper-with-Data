import os
import argparse
import pandas as pd
import json
import time
import glob
import hashlib
import chromadb
from pypdf import PdfReader

# Vertex AI
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, GenerationConfig, Content, Part, ToolConfig

# Langchain
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_experimental.text_splitter import SemanticChunker
from semantic_splitter import SemanticChunker
import agent_tools

# Setup
GCP_PROJECT = "ac215-zhiyuli"
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-001"
INPUT_FOLDER = "input-datasets"
OUTPUT_FOLDER = "outputs"
# CHROMADB_HOST = "llm-rag-chromadb"
# CHROMADB_PORT = 8000
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api#python
# embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192,  # Maximum number of tokens for output
    "temperature": 0.25,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}


SYSTEM_INSTRUCTION = "You are a helpful AI assistant. You need to help me to correct the problems in the format of texts I extract from PDF files. "

generative_model = GenerativeModel(
        GENERATIVE_MODEL,
        system_instruction=[SYSTEM_INSTRUCTION]
)



# Step 1: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text_per_page = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text_per_page.append(page.extract_text())
    return text_per_page

# Step 2: Preprocess the extracted text (optional, for text format correction)
def preprocess_text(text):
    # Handle common issues, like multiple line breaks, misplaced spaces, or missing punctuation
    INPUT_PROMPT = (
        f"Here is a text extracted from a PDF. Correct any formatting errors, including line breaks, misplaced spaces, punctuation issues, and redundant information irrelevant to the main body of the article such as page number, acknowledge, footnote and headnote:\n\n{text}\n\n Provide the corrected version below."
    )
        
    response = generative_model.generate_content(
    [INPUT_PROMPT], # Input prompt
        generation_config=generation_config, # Confiugration settings
        stream=False,
    )
    
    corrected_text = response.text
    return corrected_text

# Step 3: Define a prompt for the LLM to merge text parts with overlap
def merge_texts_prompt(prev_part, next_part):
    return (f"Here are two overlapping parts of a document. Merge them into a coherent paragraph "
            f"to ensure that the flow between the sections remains natural and logical:\n\n"
            f"Previous Part: {prev_part}\n\n"
            f"Next Part: {next_part}\n\n"
            f"Provide the merged text below.")

# Step 4: Use the LLM to merge overlapping text parts
def merge_text_parts_with_overlap(prev_part, next_part):
    INPUT_PROMPT = merge_texts_prompt(prev_part, next_part)
    
    response = generative_model.generate_content(
    [INPUT_PROMPT], # Input prompt
        generation_config=generation_config, # Confiugration settings
        stream=False,
    )
    
    merged_text = response.text
    return merged_text.strip()

# Step 5: Process the text in overlapping chunks, merging them step by step
def process_and_merge_with_overlap(text_per_page, chunk_size=3, overlap_size=1):
    # Combine pages into chunks, and ensure each chunk overlaps with the previous one
    chunks = []
    chunks = []
    for i in range(0, len(text_per_page), chunk_size - overlap_size):
        chunk = ''.join(text_per_page[i:i + chunk_size])
        processed_chunk = preprocess_text(chunk)  # Correct format for each chunk
        chunks.append(processed_chunk)
        print("process_Chunck:\n\n")
        print(processed_chunk)
        time.sleep(5)

    # Merge chunks with overlap
    # merged_text = chunks[0]
    # for i in range(1, len(chunks)):
    #     overlap_part = merged_text[-len(chunks[i-1]):]  # Extract the overlapping part
    #     merged_text = merge_text_parts_with_overlap(overlap_part, chunks[i])
    #     print("merged_text:\n\n")
    #     print(merged_text)
    return "\n".join(chunks)

# Main workflow
def main(pdf_path):
    # Extract text from the PDF (page by page)
    text_per_page = extract_text_from_pdf(pdf_path)
    
    # Process and merge the text with overlapping chunks (e.g., 3 pages per chunk, 1 page overlap)
    final_corrected_text = process_and_merge_with_overlap(text_per_page, chunk_size=3, overlap_size=1)
    
    # Output or save the final formatted text
    print("Final Merged and Corrected Text:\n", final_corrected_text)

main("./1.pdf")
