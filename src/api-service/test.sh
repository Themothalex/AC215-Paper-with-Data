#!/bin/bash

# URL of the API endpoint
URL="http://localhost:9000/search"

# Test Case 1: Valid Input
echo "Test Case 1: Valid Input"
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "independent_variable": "Age",
        "dependent_variable": "Health",
        "region": "USA",
        "data_unit": "Years"
    }' \
    $URL
echo -e "\n"

# Test Case 2: Missing All Fields (Should Return 400)
echo "Test Case 2: Missing All Fields"
curl -X POST -H "Content-Type: application/json" \
    -d '{}' \
    $URL
echo -e "\n"

# Test Case 3: Input with No Matches (Should Return 404)
echo "Test Case 3: Input with No Matches"
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "independent_variable": "Unknown",
        "dependent_variable": "Unknown",
        "region": "Unknown",
        "data_unit": "Unknown"
    }' \
    $URL
echo -e "\n"

# Test Case 4: Partial Input
echo "Test Case 4: Partial Input"
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "independent_variable": "Age"
    }' \
    $URL
echo -e "\n"
