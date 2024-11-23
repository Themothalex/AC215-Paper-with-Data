import unittest
from unittest.mock import MagicMock, patch
from text_processor import (
    process_pdf_from_gcs,
    preprocess_text,
    c,
    bucket_exists,
)


class TestTextProcessor(unittest.TestCase):
    @patch("text_processor.PdfReader")
    def test_process_pdf_from_gcs(self, mock_pdf_reader):
        # Simulate the behavior of PdfReader
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Sample PDF text"
        mock_pdf_reader.return_value.pages = [mock_page] * 2

        # Mock GCS byte download
        with patch("text_processor.storage.Client") as mock_storage_client:
            mock_blob = MagicMock()
            mock_blob.download_as_bytes.return_value = b"%PDF-1.4"

            mock_bucket = MagicMock()
            mock_bucket.blob.return_value = mock_blob

            mock_storage_client.return_value.bucket.return_value = mock_bucket

            # Call the function
            result = process_pdf_from_gcs("mock_bucket", "mock_blob")
            self.assertEqual(result, ["Sample PDF text", "Sample PDF text"])

    def test_preprocess_text(self):
        # Mock LLM content generation
        with patch(
            "text_processor.GenerativeModel.generate_content"
        ) as mock_generate:
            mock_response = MagicMock()
            mock_response.text = "Corrected Text"
            mock_generate.return_value = mock_response

            input_text = "Sample PDF extracted text"
            result = preprocess_text(input_text)
            self.assertEqual(result, "Corrected Text")

    @patch("text_processor.storage.Client")
    def test_c(self, mock_storage_client):
        # Mock GCS client and blob behavior
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        # Call the function
        c("mock_bucket", "Sample content", "sample_blob.txt")

        # Assert methods were called as expected
        mock_bucket.blob.assert_called_once_with("sample_blob.txt")
        mock_blob.upload_from_file.assert_called_once()

    @patch("text_processor.storage.Client")
    def test_bucket_exists(self, mock_storage_client):
        # Mock get_bucket to succeed
        mock_storage_client.return_value.get_bucket.return_value = MagicMock()

        # Call the function and assert True is returned
        self.assertTrue(bucket_exists("existing_bucket"))

        # Mock get_bucket to raise an exception
        mock_storage_client.return_value.get_bucket.side_effect = Exception(
            "Bucket not found"
        )

        # Call the function and assert False is returned
        self.assertFalse(bucket_exists("nonexistent_bucket"))


if __name__ == "__main__":
    unittest.main()
