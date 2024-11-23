# How to run the workflow

## Run script to build images and three containers

### Container1 text_processor do the following 
1.1 extract text from pdf files \
1.2 format text using LLM \
1.3 store text files

### Container2 featureExtracter do the following 
2.1 10 examples (by human or by chatgpt) in database \
2.2 using the the new article to retrieve the most similar one from the example database \
2.3 put the example  into the prompt to instruct the LLM to extract features from the new article according to the example 

### Container3 rag do the following
3.1 embed all the files of extracted features \
3.2 embed the query and calculate the similarity between the query and files in the database \
3.3 rank and return the ranked results

This will build the image and start all three container using docker compose
```
sh docker-shell.sh
```

## Run the entire workflow

```
sh workflow.sh
```

