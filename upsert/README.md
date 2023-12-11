### Upsert data

The AI assistant uses ChromaDB as the vector database. More information about Chroma can be found [here](https://docs.trychroma.com/).
Please refer to details of the project [here](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/blob/main/README.md) before proceeding with these steps.

#### Configure settings

* Before running the application, configure the config.yaml file to specify the local vector chroma database settings and the path to the data files.
* We have provided the CPIC data we used for this pilot in the "data" folder, including CSVs and publications. If required you can replace these files with your own.
* Replace the following lines in the config.yaml file with the appropriate file paths:
* You can customize the chunk size and overlap size in the config.yaml file for the PDF files.

####  Prepare source mapping
[source_metadata_mapping.py](source_metadata_mapping.py) contains metadata for all data files you use. It should be updated according to data files.

```commandline
chromadb:
  persist_directory: /path/to/chroma-db/persist  # directory to persist the database
  chroma_db_impl: duckdb+parquet # database implementation
  collection_name: slco1b1_collection  # name of the collection

data:
  directory:
    - /path/to/data/slco1b1/csvs
    - /path/to/data/slco1b1/pdfs

parse_pdf:
  chunk_size: 1000  # number of characters per chunk
  chunk_overlap: 50  # number of characters to overlap between chunks
```
####  Insert data into the vector database
* Run the following command to insert the data into the vector database (Only run it once for the same config.yaml file):
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/upsert
3. python upsert_chroma.py -y ../config.yaml
```

#### Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```
Please ensure you use the same config.yaml file for both data insertion and question/answering. Please note that the first time you run the application, there might be a lag for data to be loaded into the vector database. 
