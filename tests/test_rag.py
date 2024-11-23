import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from featureExtracter import generate_embedding, find_best_match


# Test for generate_embedding with a mocked model
@patch("featureExtracter.embedding_model")
def test_generate_embedding(mock_embedding_model):
    # Mock the embedding model's output
    mock_embedding = MagicMock()
    mock_embedding.get_embeddings.return_value = [
        MagicMock(values=[0.1, 0.2, 0.3])
    ]
    mock_embedding_model.return_value = mock_embedding

    input_text = "Sample text for embedding"
    expected_embedding = np.array([0.1, 0.2, 0.3])

    # Run the function
    result = generate_embedding(input_text)

    # Assert the result matches the mocked embedding
    np.testing.assert_array_equal(result, expected_embedding)


# Test for find_best_match with mocked embeddings
@patch("featureExtracter.generate_embedding")
@patch("featureExtracter.cosine_similarity")
def test_find_best_match(mock_cosine_similarity, mock_generate_embedding):
    # Mock the embedding and similarity computation
    mock_generate_embedding.side_effect = lambda x: np.array([0.1, 0.2, 0.3])
    mock_cosine_similarity.side_effect = lambda x, y: [[0.95]]

    input_text = "Test input text"
    json_embeddings = [
        {"path": "data/feature_1.json", "embedding": np.array([0.4, 0.5, 0.6])}
    ]

    # Run the function
    best_match, best_score = find_best_match(input_text, json_embeddings)

    # Assert the best match and score are correct
    assert best_match == json_embeddings[0]
    assert best_score == 0.95
