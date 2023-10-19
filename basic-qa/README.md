### Basic QA
Assuming that data has been successfully inserted into the vector database (chromadb), this application will retrieve contextual information from the vector database. This retrieval is based on the user's current question. Subsequently, this contextual information is leveraged to generate an answer to the user's question.


#### 1. Question and Answering
* Assume that the data have been inserted into vector database(chromadb), run the following commands to start the question and answering application. The application will load the data from the vector database and initiate the Q&A session.
* For patients:
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/basic-query
3. python questions_answering.py -y /path/to/config.yaml -r patient
```
* For providers:
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/basic-query
3. python questions_answering.py -y /path/to/config.yaml -r provider
```
* To exit a Q&A session, simply type 'exit'.
#### 2. Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```