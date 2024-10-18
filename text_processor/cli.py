import os
from google.cloud import storage
from pypdf import PdfReader
import io
import time
import vertexai
from vertexai.generative_models import GenerativeModel

# set the parameters of Google Cloud and Vertex AI
GCP_PROJECT = "ac215-438315"
GCP_LOCATION = "us-east1"
GENERATIVE_MODEL = "gemini-1.5-flash-001"
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# set config
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.25,
    "top_p": 0.95,
}

SYSTEM_INSTRUCTION = "You are a helpful AI assistant. You need to help me correct the problems in the format of texts I extract from PDF files."

generative_model = GenerativeModel(
    GENERATIVE_MODEL,
    system_instruction=[SYSTEM_INSTRUCTION]
)

# extract text from pdf files after reading pdf files from GCS
def process_pdf_from_gcs(bucket_name, pdf_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(pdf_blob_name)
    
    # read byte stream from GCS
    pdf_bytes = blob.download_as_bytes()

    # read PDF files
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text_per_page = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text_per_page.append(page.extract_text())
    
    return text_per_page

# form text files using LLM
def preprocess_text(text):
    input_prompt = (
        f"Here is a text extracted from a PDF. Correct any formatting errors, including line breaks, misplaced spaces, punctuation issues, garbled code and redundant information irrelevant to the main body of the article such as page number, acknowledge, footnote and headnote:\n\n {text}\n\n Provide the corrected version below."
    )
    response = generative_model.generate_content(
        [input_prompt],
        generation_config=generation_config,
        stream=False,
    )
    return response.text

# upload text files to Google Cloud Storage
def upload_txt_to_gcs(bucket_name, content, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    with open("./to_upload.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    with open("./to_upload.txt", "r", encoding="utf-8") as f:
        blob.upload_from_file(f, content_type="text/plain")
    print(f"Uploaded {destination_blob_name} to gs://{bucket_name}/{destination_blob_name}")

# process pdf files and upload text files
def process_and_upload_pdfs(input_bucket_name, output_bucket_name, chunk_size=3):
    client = storage.Client()
    input_bucket = client.bucket(input_bucket_name)
    
    # get the names of all pdf files in the bucket
    blobs = input_bucket.list_blobs()
    
    for blob in blobs:
        time.sleep(15)
        if blob.name.endswith(".pdf"):
            print(f"Processing {blob.name}")
            text_per_page = process_pdf_from_gcs(input_bucket_name, blob.name)

            # format text files
            formatted_text = []
            page = 1
            for i in range(0, len(text_per_page), chunk_size):
                chunk = "".join(text_per_page[i:i + chunk_size])
                corrected_text = preprocess_text(chunk)
                formatted_text.append(corrected_text)
                time.sleep(7)  
                print(page)
                page += 1 
            # merge formatted text files and upload
            final_text = "\n".join(formatted_text)
            txt_filename = blob.name.replace(".pdf", ".txt")
            upload_txt_to_gcs(output_bucket_name, final_text, txt_filename)


def main():
    input_bucket_name = "original_pdf_data"
    output_bucket_name = "original_txt"  
    
    # process text files and upload
    process_and_upload_pdfs(input_bucket_name, output_bucket_name)

if __name__ == "__main__":
    main()

