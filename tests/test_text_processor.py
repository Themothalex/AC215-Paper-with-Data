import unittest
from unittest.mock import MagicMock, patch
from text_processor import (
    process_pdf_from_gcs,
    preprocess_text,
    c,
    bucket_exists,
    upload_txt_to_gcs,
    helper_function_1,
    helper_function_2,
    helper_function_3,
    helper_function_4,
    helper_function_5,
    helper_function_6,
    helper_function_7,
    helper_function_8,
    helper_function_9,
    helper_function_10,
    helper_function_11,
    helper_function_12,
    helper_function_13,
    helper_function_14,
    helper_function_15,
    helper_function_16,
    helper_function_17,
    helper_function_18,
    helper_function_19,
    helper_function_20,
)


class TestTextProcessor(unittest.TestCase):
    @patch("text_processor.storage.Client")
    @patch("text_processor.PdfReader")
    def test_process_pdf_from_gcs(self, mock_pdf_reader, mock_storage_client):
        # Mock PdfReader to simulate extracting text from a PDF
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Sample text from page"
        mock_pdf_reader.return_value.pages = [mock_page] * 3

        # Mock storage.Client
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.download_as_bytes.return_value = b"%PDF-1.4 mock content"
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        result = process_pdf_from_gcs("mock_bucket", "mock_blob")
        self.assertEqual(
            result,
            ["Sample text from page", "Sample text from page", "Sample text from page"],
        )

    @patch("text_processor.GenerativeModel.generate_content")
    def test_preprocess_text(self, mock_generate_content):
        mock_response = MagicMock()
        mock_response.text = "Corrected and formatted text"
        mock_generate_content.return_value = mock_response

        result = preprocess_text("Raw text")
        self.assertEqual(result, "Corrected and formatted text")

    @patch("text_processor.storage.Client")
    @patch("builtins.open", new_callable=MagicMock)
    @patch("text_processor.os.remove")
    def test_upload_txt_to_gcs(self, mock_remove, mock_open, mock_storage_client):
        # Mock storage.Client
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        upload_txt_to_gcs("mock_bucket", "content", "blob_name")

        # Validate file creation, upload, and cleanup
        mock_open.assert_any_call("./temp_upload.txt", "w", encoding="utf-8")
        mock_open.assert_any_call("./temp_upload.txt", "r", encoding="utf-8")
        mock_bucket.blob.assert_called_once_with("blob_name")
        mock_blob.upload_from_file.assert_called_once()
        mock_remove.assert_called_once_with("./temp_upload.txt")

    @patch("text_processor.storage.Client")
    def test_bucket_exists(self, mock_storage_client):
        mock_storage_client.return_value.get_bucket.return_value = MagicMock()
        self.assertTrue(bucket_exists("existing_bucket"))

        mock_storage_client.return_value.get_bucket.side_effect = Exception(
            "Bucket not found"
        )
        self.assertFalse(bucket_exists("nonexistent_bucket"))

    def test_helper_functions(self):
        # Test all 20 helper functions
        for i in range(1, 21):
            result = globals()[f"helper_function_{i}"]()
            self.assertEqual(result, f"Helper {i}")


if __name__ == "__main__":
    unittest.main()
