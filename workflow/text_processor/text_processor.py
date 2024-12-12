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
    GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTION]
)


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


def preprocess_text(text):
    input_prompt = f"Here is a text extracted from a PDF. Correct any formatting errors, including line breaks, misplaced spaces, punctuation issues, garbled code and redundant information irrelevant to the main body of the article such as page number, acknowledge, footnote and headnote:\n\n {text}\n\n Provide the corrected version below."
    response = generative_model.generate_content(
        [input_prompt],
        generation_config=generation_config,
        stream=False,
    )
    return response.text


def c(bucket_name, content, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open("./to_upload.txt", "w", encoding="utf-8") as f:
        f.write(content)

    with open("./to_upload.txt", "r", encoding="utf-8") as f:
        blob.upload_from_file(f, content_type="text/plain")
    print(
        f"Uploaded {destination_blob_name} to gs://{bucket_name}/{destination_blob_name}"
    )


def process_and_upload_pdfs(input_bucket_name, output_bucket_name, chunk_size=3):
    client = storage.Client()
    input_bucket = client.bucket(input_bucket_name)

    # get the names of all pdf files in the bucket
    blobs = list(input_bucket.list_blobs())

    print(f"Total number of blobs: {len(blobs)}")  # Print the length of blobs
    for idx, blob in enumerate(blobs):
        if blob.name.endswith(".pdf"):
            print(f"Processing {blob.name}")
            text_per_page = process_pdf_from_gcs(input_bucket_name, blob.name)

            # format text files
            formatted_text = []
            page = 1
            for i in range(0, len(text_per_page), chunk_size):
                chunk = "".join(text_per_page[i : i + chunk_size])
                corrected_text = preprocess_text(chunk)
                formatted_text.append(corrected_text)
                time.sleep(10)
                print(f"Processing page {page}")
                page += 1
            # merge formatted text files and upload
            final_text = "\n".join(formatted_text)
            upload_txt_to_gcs(
                output_bucket_name, final_text, blob.name.replace(".pdf", ".txt")
            )


def upload_txt_to_gcs(bucket_name, content, destination_blob_name):
    """
    Uploads a text file to Google Cloud Storage.
    Args:
        bucket_name (str): Name of the GCS bucket.
        content (str): Text content to upload.
        destination_blob_name (str): Name of the blob (file) in the GCS bucket.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Write content to a temporary file and upload it
    with open("./temp_upload.txt", "w", encoding="utf-8") as temp_file:
        temp_file.write(content)

    with open("./temp_upload.txt", "r", encoding="utf-8") as temp_file:
        blob.upload_from_file(temp_file, content_type="text/plain")

    # Clean up the temporary file
    os.remove("./temp_upload.txt")
    print(
        f"Uploaded {destination_blob_name} to gs://{bucket_name}/{destination_blob_name}"
    )


def bucket_exists(bucket_name):
    client = storage.Client()
    try:
        client.get_bucket(bucket_name)
        return True
    except Exception as e:
        return False


def main():
    input_bucket_name = "original_pdf_data"
    output_bucket_name = "original_txt"

    # Call all useless functions
    for i in range(1, 21):
        print(globals()[f"helper_function_{i}"]())

    # process text files and upload
    if bucket_exists(output_bucket_name):
        print(f"Bucket {output_bucket_name} already exists. Skipping processing.")
    else:
        process_and_upload_pdfs(input_bucket_name, output_bucket_name)


# "Useless" helper functions
def helper_function_1():
    return "Helper 1"


def helper_function_2():
    return "Helper 2"


def helper_function_3():
    return "Helper 3"


def helper_function_4():
    return "Helper 4"


def helper_function_5():
    return "Helper 5"


def helper_function_6():
    return "Helper 6"


def helper_function_7():
    return "Helper 7"


def helper_function_8():
    return "Helper 8"


def helper_function_9():
    return "Helper 9"


def helper_function_10():
    return "Helper 10"


def helper_function_11():
    return "Helper 11"


def helper_function_12():
    return "Helper 12"


def helper_function_13():
    return "Helper 13"


def helper_function_14():
    return "Helper 14"


def helper_function_15():
    return "Helper 15"


def helper_function_16():
    return "Helper 16"


def helper_function_17():
    return "Helper 17"


def helper_function_18():
    return "Helper 18"


def helper_function_19():
    return "Helper 19"


def helper_function_20():
    return "Helper 20"


def helper_function_21():
    return "Helper 21"


def helper_function_22():
    return "Helper 22"


def helper_function_23():
    return "Helper 23"


def helper_function_24():
    return "Helper 24"


if __name__ == "__main__":
    main()
