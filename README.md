### Pharmacogenetic AI Assistant for Genetic Counseling and Personalized Care

The PGx AI Assistant is a proof of concept (POC) pilot project that explores the potential of OpenAI's GPT-4 in the field of genetic counseling and personalized care. The primary objective of this project is to develop an AI assistant that aids both patients and healthcare providers with addressing knowledge gaps, ultimately enhancing the accessibility and comprehension of genetic test results. This POC is tailored for a specific use case in pharmacogenetic (PGx) testing, with particular emphasis on SLCO1B1 diplotypes and statins.

#### Technology Overview:
The PGx AI Assistant leverages large language models, making use of GPT-4's context-aware capabilities and retrieval augmented generation (RAG) methodology. By integrating the strengths of retrieval-based and generative methods, the AI assistant is equipped to provide responses that are contextually relevant and aligned with the specific queries it receives.

#### Contextual Knowledge Base
To support the AI assistant's understanding of pharmacogenetic testing and statins, a contextual knowledge base was created. This knowledge base consists of the CPIC dataset for statins and relevant publications. The dataset can be found in the "data" folder of this GitHub repository.

#### Utilizing Embeddings for Context Retrieval
The contextual knowledge base is transformed into embeddings using OpenAI's 'text-embedding-ada-002' model, specifically designed for context retrieval. These embeddings are then stored in a Chroma vector database. When a patient or provider submits a query to the AI assistant, the query is converted into embeddings. Pertinent information related to the query is then retrieved from the vector database. This contextual information, along with the user's query and appropriate prompts based on the user's role, is passed to GPT-4.

#### Prompts for Accuracy and Customization
To ensure accuracy and relevance in the AI assistant's responses, prompts are carefully engineered. These prompts serve two essential purposes:
Constraining GPT-4's Responses: The prompts limit the scope of GPT-4's responses to the provided context, ensuring that the generated answers are within the context of the query.
Customizing Language and Tone: The prompts adapt the language and tone of the AI assistant's responses based on whether the user is a patient or a healthcare provider, providing a personalized response.

#### Challenges and Mitigations
A significant challenge we encountered during the POC was related to the OpenAI "text-embedding-ada-002" model's occasional inability to recognize diplotype terms like '*1/*1', resulting in contextual inaccuracies. It is worth noting that these large language models are not specifically pre-trained on biomedical knowledge, hence this limitation was not entirely unexpected. To address this concern in future developments, we intend to explore biomedical models that may offer more domain-specific understanding.

For this POC, we navigated around the issue by implementing constraints on GPT-4's responses. We ensured that answers were provided only when supported by contextual information, significantly reducing the impact of inaccuracies. However, it is essential to acknowledge that some potential for confabulation and hallucination remains despite our efforts to minimize inaccuracies. As we move forward, we will continue to refine our approach to enhance the AI assistant's performance in this regard.

#### Project Results and Future Potential
Despite the encountered challenges, this POC showcased the remarkable potential of GPT-4 in augmenting genetic counseling and personalized care. The AI assistant, for the most part, delivered precise and pertinent responses, promising to a substantial improvement in the accessibility and comprehension of genetic test results.

For a comprehensive understanding of this project, including additional insights gained, lessons learned, and an evaluation of the results, please refer to the preprint document [add reference]. This document provides a detailed account of the project's journey, contributing to the broader knowledge base in the field of genetic counseling and personalized care.

As we move forward, we envision further refinements and innovations in this technology, leveraging GPT-4's capabilities, and exploring advancements in biomedical models.

### Getting Started with the PGx AI assistant
To get started with this project and run your own queries, follow the step-by-step walkthrough below. Please keep in mind that the contextual dataset is limited to SLOCO1B1 and statins, so all questions should be related to this specific area. We have included sample questions in patient-questions.py and provider_questions.py for your reference.

#### 1. Check out the project
* Create a new folder for the project.
* Navigate to the project folder using  command line.
* Clone the repository into the folder using the following command:
```commandline
cd </path/to/project>
git clone https://github.com/BCM-HGSC/PGx-slco1b1-chatbot.git
```
#### 2. Setup python environment
* We recommend using miniconda to manage the virtual environment. If you don't have miniconda installed, you can download it [here](https://docs.conda.io/en/latest/miniconda.html).
* After installing miniconda, create a virtual environment and install the required packages with the following commands:
```
1. conda create -n "<virtual-environment-name>" python=3.11.4 ipython
2. conda activate <virtual-environment-name>
3. pip install --upgrade pip
4. pip install -r requirements.txt
```
#### 3. Configure OpenAI settings
* The application utilizes the OpenAI API for embedding and querying.
* Replace the following lines in the config.yaml file with your OpenAI account's secret key, available on the [website](https://platform.openai.com/account/api-keys). You might use different models for embedding and chat. 
The default models are text-embedding-ada-002 and gpt-4. 
You can change the models in the config.yaml file. 
* Also you can change the search type and number of resources to pickup.
```commandline
openai:
  api_key: xxxx
  embedding_model_name: text-embedding-ada-002
  chat_model_name: gpt-4
  chat_search_type: mmr   # mmr or similarity
  chat_search_k: 4        # number of best resources to pickup
```
For security we recommend setting the OPENAI_API_KEY as an environment variable before running the application. See instructions here [website](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).
```
export OPENAI_API_KEY='sk-xxxx'
```

#### 4. Insert data into the vector database
* See [upsert](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/blob/main/upsert/README.md) for details

#### 5. Question and Answering
* Once the data insertion is complete, two options to do question/answering.
  * For basic QA, use [basic-qa](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/basic-qa).
  * For broswer QA, use [chatbot-stream](https://github.com/BCM-HGSC/PGx-slco1b1-chatbot/tree/main/chatbot-stream).

#### 6. Deactivate Virtual Environment:
* After using the application, deactivate the virtual environment with the following command:
```commandline
conda deactivate  
```
Please ensure you use the same config.yaml file for both data insertion and question/answering. Please note that the first time you run the application, there might be a lag for data to be loaded into the vector database. Enjoy using the PGx-slco1b1-chatbot! If you encounter any issues or have questions, feel free to reach out for support.
