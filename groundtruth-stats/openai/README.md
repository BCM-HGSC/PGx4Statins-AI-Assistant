### Ground Truth

Assuming that the data, which can be found [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/groundtruth-stats/data), has been successfully incorporated into the vector database known as "chromadb" (for information on how to upsert data into the vector store, please refer to this [link](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/upsert), you need a new source_metadata_mapping.py for new data files ), this application is designed to utilize a list of questions and retrieve the most relevant contextual information from the vector database for each question. Subsequently, it will assess the retrieved information to determine if it matches the questions. You can designate the corresponding cells as "matches" (e.g., set them to 1) for the best-matching documents and as "non-matches" (e.g., set them to 0) for the rest.

#### 1. Run the script  
* We assume the test data have been upserted into vector store chromadb, run the following commands to get ground truth results, which include [final_summary.csv](final_summary.csv), [final_individual_summary.csv](final_individual_summary.csv) and more detailed information in different txt and csv files.
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