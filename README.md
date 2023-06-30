### About PGx-slco1b1-chatbot

The project described aims to explore the potential of GenAI, specifically GPT-4, in the field of genetic counseling and personalized care. The primary objective is to improve the accessibility and interpretation of genetic test results, with a specific focus on genetic testing for predicting responses to drug therapies.

By leveraging the capabilities of GenAI, the project seeks to enhance the process of genetic counseling, making it more efficient and effective for both patients and healthcare providers. This technology has the potential to assist in the interpretation of complex genetic data, providing valuable insights into the predicted response to drug therapies. This, in turn, can contribute to personalized care plans that are tailored to individual patients based on their genetic makeup.

In addition to improving accessibility and interpretation, the project also recognizes the importance of addressing the risks associated with the adoption of GenAI. Patient safety is a critical concern, and the study aims to evaluate and implement practical safeguards to mitigate these risks. By doing so, the project seeks to ensure that the integration of GenAI into clinical practice is responsible and safe for patients.

The overall goal of this project is to gain a comprehensive understanding of how GenAI can enhance personalized care in the field of clinical genetics. By utilizing this innovative technology, the project aims to reduce disparities in accessing genetic information, promote equitable access to personalized care, and ultimately improve patient outcomes.

### Getting Started with PGx-slco1b1-chatbot
#### Check out the project
You might create a new folder for the project and check out the project in the folder:
```commandline
cd </path/to/project>
git clone https://github.com/BCM-HGSC/PGx-slco1b1-chatbot.git
```
#### Setup python environment

Since packages need python version >=3.7 and <3.10, we recommend creating python virtual environment with python 3.9. 

```
1. cd </path/to/project/>PGx-slco1b1-chatbot
2. python3.9 -m venv <virtual-environment-name>
3. source <virtual-environment-name>/bin/activate
4. pip install --upgrade pip
5. pip install -r requirements.txt
```

#### Run the project
Before running the application, somethings need to be configured in the config.yaml file. You can specify the local vector chroma database settings and the path to the data files in the config.yaml file. We provide some data files in data folder, which includes some csv and pdf files for demo. For the pdf file, the chunk size and overlap size are configurable in the config.yaml file. You can replace the following line in the config.yaml file:
```commandline
data:
  directory:
    - data/slco1b1/csvs
    - data/slco1b1/pdfs

parse_pdf:
  chunk_size: 500
  chunk_overlap: 100

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
  persist_directory: chroma-db/persist
  chroma_db_impl: duckdb+parquet
  collection_name: slco1b1_collection
```
You can run the following command to insert the data into the vector database:
```
1. cd </path/to/project>/PGx-slco1b1-chatbot
2. source <virtual-environment-name>/bin/activate
3. python upsert.py -y config.yaml
```

##### Question and Answering
You can run the following command to start the question and answering application:
```
1. cd </path/to/project>/PGx-slco1b1-chatbot
2. source <virtual-environment-name>/bin/activate
3. python question_answering.py -y config.yaml
```
Note: The first time you run the application, it will take some time to load the data into the vector database. 

Note:  You should use the same config.yaml file for the upsert.py and question_answering.py.

Enjoy it!