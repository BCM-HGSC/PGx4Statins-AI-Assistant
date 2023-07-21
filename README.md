### About the PGx AI Assistant 

This proof of concept(POC) pilot project aims to explore the potential of OpenAI's GPT-4, in the field of genetic counseling and personalized care. The primary objective of this project was to develop an AI assistant targeted to both patients and healthcare providers to help fill knowledge gaps and respond to user queries for a specific use case in pharmacogenetic (PGx) testing, with a focus on SLCO1B1 diplotypes and statins, with the goal of improving the accessibility and interpretation of genetic test result. The AI assistant leverages context-aware GPT-4 and retrieval augmented generation (RAG). RAG builds on both retrieval based and generative methods thereby providing the appropriate context required for GPT-4's responses.

For this POC, we created a contextual knowledge base that consisted of the CPIC dataset for statins and related publications. The dataset is available in the data folder of this github repo. Next we created embeddings for this dataset using OpenAI's 'text-embedding-ada-002' model for context retrieval. These embeddings are stored in a Chroma vector database. Patient of provider queries to the AI assistant are converted into embeddings and pertinent information related to the query is retrieved from the vector database. This contextual information along with the user's query and appropriate prompts based on the role of the user is passed to GPT-4. The prompts provide safeguards for constraining the scope of GPT-4's responses to the provided context, and also customizes the language and tone of the response based on the role of the user. This resulted in responses that were for the most part accurate and relevant. However we did observe a discrepancy with the OpenAI's "text-embedding-ada-002" embedding model. Specific diplotype terms such as '*1/*1' were not recognized by the embedding model resulting in inaccurate contextual information. However as we constrained the GPT-4's responses via prompt engineering to respond only if an answer was avaiable, we were able to avoid inaccurate responses for the most part though the potential for confabulation and hallucination was still present. Even with this and other challenges, overall, this project demonstrated the immense potential of GPT-4 for augmenting an area such as genetic counseling and personalized care. Information about this project including other lessons learned, challenges etc is illustrated in this preprint <add reference>.

The steps below provide a walkthrough of setting this project up locally and executing your own queries. Please note that the contextual dataset is constrained to SLOCO1B1 and statins so questions have to be related to that area. We have provided some sample questions in patient-questions.py and provider_questions.py for your reference.

### Getting Started with PGx-slco1b1-chatbot
#### Check out the project
You might create a new folder for the project and check out the project in the folder:
```commandline
cd </path/to/project>
git clone https://github.com/BCM-HGSC/PGx-slco1b1-chatbot.git
```
#### Setup python environment

Since some python packages need python version >=3.7 and <=3.10, we recommend creating python virtual environment with python 3.9. We use miniconda to manage python virtual environment. You can download miniconda from [here](https://docs.conda.io/en/latest/miniconda.html). After installing miniconda, you can create a virtual environment and install the required packages by running the following commands:

```
1. conda create -n "<virtual-environment-name>" python=3.9.2 ipython
2. conda activate <virtual-environment-name>
3. pip install --upgrade pip
4. pip install -r requirements.txt
```

#### Run the project
Before running the application, somethings need to be configured in the config.yaml file. You can specify the local vector chroma database settings and the path to the data files in the config.yaml file. We provide some data files in data folder, which includes some csv and pdf files for demo. For the pdf file, the chunk size and overlap size are configurable in the config.yaml file. You can replace the following line in the config.yaml file:
```commandline
data:
  directory:
    - /path/to/data/slco1b1/csvs
    - /path/to/data/slco1b1/pdfs

parse_pdf:
  chunk_size: 1000  # number of characters per chunk
  chunk_overlap: 50  # number of characters to overlap between chunks

```
Since we use openai api to do embedding and querying, your account's secret key which is available on the [website](https://platform.openai.com/account/api-keys) is needed. You can replace the following line in the config.yaml file:
```
openai:
  api_key: sk-xxxx
```

But we recommand you set it as the OPENAI_API_KEY environment variable before running the application:
```
export OPENAI_API_KEY='sk-xxxx'
```

##### Insert the data into the vector database
We choose Chroma as the vector database. You can find more information about Chroma [here](https://docs.trychroma.com/). We provide a script to insert the data into the vector database, For making things simple, we configure Chroma to save and load from local machine. Data will be persisted on exit and loaded on start (if it exists). You can replace the following line in the config.yaml file:
```commandline
chromadb:
  persist_directory: /path/to/chroma-db/persist  # directory to persist the database
  chroma_db_impl: duckdb+parquet # database implementation
  collection_name: slco1b1_collection  # name of the collection
```
You can run the following command to insert the data into the vector database(You only need to run it once for the same config.yaml file)
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/upsert
3. python upsert.py -y ../config.yaml
```

##### Question and Answering
Once you complete data insertion, you can run the following command to start the question and answering application, which will load the data from the vector database and start the question and answering loop:

For patient:
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot
3. python questions_answering.py -y config.yaml -r patient
```
For provider:
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot
3. python questions_answering.py -y config.yaml -r provider
```
Typing 'exit' to exit the Question/Answering loop. And you can deactivate the virtual environment by running the following command:
```commandline
conda deactivate  
```

Note: The first time you run the application, it will take some time to load the data into the vector database. 

Note:  You should use the same config.yaml file for the upsert and questions/answering.

Enjoy it!
