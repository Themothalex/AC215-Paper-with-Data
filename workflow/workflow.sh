
#!/bin/bash

# set -e -x

# Extract and convert PDFs to TxTs
echo "Running container text_processor"
docker exec -it text_processor pipenv run python text_processor.py

# instruct the LLM to extract features from the new article according to the example
echo "Running container featureExtracter"
docker exec -it featureExtracter pipenv run python featureExtracter.py

# Embedding files and return the ranked results
echo "Running container embedding"
docker exec -it embedding pipenv run python embedding.py


