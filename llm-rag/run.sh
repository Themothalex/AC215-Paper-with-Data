#!/bin/bash 

set -ex

# pip install --upgrade chromadb

# Chunk Documents
python cli.py --chunk --chunk_type char-split
python cli.py --chunk --chunk_type recursive-split

# Generate embeddings for the text chunks:
python cli.py --embed --chunk_type char-split
python cli.py --embed --chunk_type recursive-split

#Load the generated embeddings into ChromaDB:
python cli.py --load --chunk_type char-split
python cli.py --load --chunk_type recursive-split

#Query the Vector Database
python cli.py --query --chunk_type char-split
python cli.py --query --chunk_type recursive-split

# #Chat with LLM
# python cli.py --chat --chunk_type char-split
# python cli.py --chat --chunk_type recursive-split

# #Advanced RAG: Semantic Chunking (Semantic Splitting)
# python cli.py --chunk --embed --load --chunk_type semantic-split

#Agents
python cli.py --agent --chunk_type char-split


