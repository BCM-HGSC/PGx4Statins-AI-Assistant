### Ground Truth

The main purpose of the section is to create a ground truth results based on the best matching documents for a set of questions. 
We use following processes to achieve this goal:
    
    Load the question set: 
        Load a list of questions that need to be evaluated.
    
    Access the "chromadb" vector database: 
        Retrieve the (5, 10, or 20) best-matching (similarity or mmr) documents for each question.

    Create the Ground Truth Matrix:
        Initialize an empty matrix with dimensions (number of questions) x (number of documents).
        For each question, find the best-matching documents based on some similarity or relevance 
        score. This could involve using techniques like cosine similarity, mmr, or other text 
        matching methods.
        Populate the matrix based on the best-matching documents. You can mark the corresponding 
        cells as "match" (e.g., set it to 1) for the best-matching documents 
        and "not a match" (e.g., set it to 0) for the rest.

    Output results to files.

#### 1. Run the script  
* We assume the test data have been upserted into vector store chromadb (if you want to know how to upsert data into vector store, please refer to [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/upsert))
, run the following commands to start ground truth application. 
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/groundtruth-stats/openai
3. python groundtruth.py -y path/to/config.yaml
```
Note: the config.yaml should be the same as the one used for upserting data into vector store.

#### 2. Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```