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


#!/bin/bash

# echo "Container is running!!!"

# # Optionally upgrade/install dependencies if needed
# # pipenv run pip install --upgrade chromadb

# # Capture any arguments passed to the script
# args="$@"
# echo "Arguments passed: $args"

# # If no arguments are passed, run a default command instead of launching an interactive shell
# if [[ -z ${args} ]]; 
# then
#     echo "No arguments passed. Running default command..."
#     # Example of running a default command like starting your application
#     pipenv run python your_default_script.py  # Replace with your default script or command
# else
#     # If arguments are passed, execute them with pipenv run
#     echo "Running the passed arguments..."
#     pipenv run python $args
# fi
