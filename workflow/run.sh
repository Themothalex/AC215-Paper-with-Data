#!/bin/bash

set -e

EXEC=embedding.py

# Run the script within the Pipenv environment
pipenv run python $EXEC
