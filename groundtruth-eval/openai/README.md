###  Performance Evaluation of the "text-embedding-ada-002" Model for PGx Context Retrieval

#### Goal:
In this section, our objective was to assess the performance of the OpenAI "text-embedding-ada-002" model in the retrieval of related context for queries posed by users against a curated KB of data and publications for statins and the genes SLCO1B1, ABCG2, and CYP2C9 based on CPIC guidelines. This retrieved context was included in the prompt to the PGx AI Assistant, see [home](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot) for more details.

The curated KB that was used for this evaluation can be found [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/groundtruth-stats/data). This KB was converted into embeddings using OpenAI "text-embedding-ada-002" model and was loaded into a ChromaDB, instructions on upserting data into the Chroma vector store, can be found [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/upsert).

#### Ground Truth:
To ensure a robust evaluation, we constructed a ground truth. This dataset provided a benchmark for comparison, focusing on key categories like diplotype and phenotype recognition.

Assuming that the data, which can be found [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/groundtruth-stats/data), has been successfully incorporated into the vector database known as "chromadb" (for information on how to upsert data into the vector store, 
please refer to this [link](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/upsert), you need a new source_metadata_mapping.py for new data files ), 
this application is designed to utilize a list of questions and 
retrieve the most relevant contextual information from the vector 
database for each question. Subsequently, it will assess the retrieved 
information to determine if it matches the questions. We designate 
the corresponding cells as "matches" (e.g., set them to 1) for 
the regular expression matching documents and question, and as "non-matches" (e.g., set them to 0) 
if not.

#### 1. Run the script  
* We assume the test data have been upserted into vector store chromadb, run the following commands to get ground truth results, which include [final_summary.csv](final_summary.csv), [final_individual_summary.csv](final_individual_summary.csv) and more detailed information in different txt and csv files.
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/groundtruth-stats/openai
3. python ground_truth.py -y path/to/config.yaml
```
Note: the config.yaml should be the same as the one used for upserting data into vector store.

#### 2. Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```
