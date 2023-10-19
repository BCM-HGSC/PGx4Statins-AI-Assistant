### Upsert data

The AI assistant uses Chroma as the vector database. More information about Chroma can be found [here](https://docs.trychroma.com/).
Assuming that configuration has been set as [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/blob/main/README.md).

####  Insert data into the vector database
* Use the provided script to insert the data into the vector database. Chroma is configured to save and load data locally for simplicity.
* Data will be persisted on exit and loaded on start (if it exists). Replace the following line in the config.yaml file with the appropriate directory for persisting the database:
```commandline
chromadb:
  persist_directory: /path/to/chroma-db/persist  # directory to persist the database
  chroma_db_impl: duckdb+parquet # database implementation
  collection_name: slco1b1_collection  # name of the collection
```
* Run the following command to insert the data into the vector database (Only run it once for the same config.yaml file):
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/upsert
3. python upsert.py -y ../config.yaml
```
* A pre-created chromba-db is also available in the 'chroma-db' folder for your use.

#### Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```
Please ensure you use the same config.yaml file for both data insertion and question/answering. Please note that the first time you run the application, there might be a lag for data to be loaded into the vector database. Enjoy using the PGx-slco1b1-chatbot! If you encounter any issues or have questions, feel free to reach out for support.
