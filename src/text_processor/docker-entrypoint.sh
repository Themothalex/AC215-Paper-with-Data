#!/bin/bash

pipenv run pip install --upgrade chromadb

args="$@"
echo $args

if [[ -z ${args} ]]; 
then
    # This is for interactive use
    # pipenv shell 
    tail -f /dev/null
else
    pipenv run python $args
fi
