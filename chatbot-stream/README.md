### Using Streamlit to utilize Q&A application
Assuming that data has been successfully inserted into the vector database (chromadb), this application will retrieve contextual information from the vector database. This retrieval is based on a condensed question that is generated from the chat history and the user's current question. Subsequently, this contextual information is leveraged to generate an answer to the user's question.

The web application is built using Streamlit, and the streaming option is employed to display the results in real-time. This approach ensures that users can receive prompt and relevant responses based on their queries and the context derived from previous interactions and stored data.

#### 1.Run Streamlit 
* Running the following commands to start the question and answering application. The application will load the data from the vector database and initiate the Q&A session.
* For patients:
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/chatbot-stream
3. streamlit run streamlit_demo.py -- --yaml  /path/to/config.yaml --role patient
```
* For providers:
```
1. conda activate <virtual-environment-name>
2. cd </path/to/project>/PGx-slco1b1-chatbot/chatbot-stream
3. streamlit run streamlit_demo.py -- --yaml  /path/to/config.yaml --role provider
```
* To exit a streamlit-demo session, simply use 'ctrl + c'.
#### 2. Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```