#!/bin/bash

echo "llm Container is running!!!"

# pipenv run pip install --upgrade chromadb

args="$@"
echo $args

# if [[ -z ${args} ]]; 
# then
#     pipenv shell
# else
#   pipenv run python $args
# fi