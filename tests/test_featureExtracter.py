import pytest
import json
from unittest.mock import patch, MagicMock
from featureExtracter import read_text_file, extract_information


# Test for read_text_file function
def test_read_text_file(tmp_path):
    # Create a temporary text file
    test_file = tmp_path / "test.txt"
    test_content = "This is a test."
    test_file.write_text(test_content, encoding="utf-8")

    # Run the function and check the output
    result = read_text_file(test_file)
    assert result == test_content, f"Expected '{test_content}', got '{result}'"
