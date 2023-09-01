# -*- coding:utf-8 -*-
# Created by liwenw at 8/28/23

import sys
sys.path.insert(0, '/Users/liwenw/PycharmProjects/ai/PGx-slco1b1-chatbot/langchain/libs/langchain/')

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from omegaconf import OmegaConf
from chromadb.config import Settings
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import argparse

from templates import system_provider_template, human_provider_template, system_patient_template, human_patient_template
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


# A basic class to create a message as a dict for chat
class Message:

    def __init__(self, role, content):
        self.role = role
        self.content = content

    def message(self):
        return {
            "role": self.role,
            "content": self.content
        }


# New Assistant class to add a vector database call to its responses
class RetrievalAssistant:

    def __init__(self, config, role):
        self.config = config
        self.role = role
        self.chat_history = []

        if role == "provider":
            system_template = system_provider_template
            human_template = human_provider_template
        elif role == "patient":
            system_template = system_patient_template
            human_template = human_patient_template
        else:
            print("role not supported")
            exit()

        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ]
        self.prompt = ChatPromptTemplate.from_messages(messages)

    def get_langchain(self):
        embeddings = OpenAIEmbeddings()

        collection_name = self.config.chromadb.collection_name
        persist_directory = self.config.chromadb.persist_directory
        chroma_db_impl = self.config.chromadb.chroma_db_impl

        vectorstore = Chroma(collection_name=collection_name,
                             embedding_function=embeddings,
                             client_settings=Settings(
                                 chroma_db_impl=chroma_db_impl,
                                 persist_directory=persist_directory
                             ),
                             )

        template = (
            "Combine the chat history and follow up question into "
            "a standalone question. Chat History: {chat_history}"
            "Follow up question: {question}"
        )

        question_generate_prompt = PromptTemplate.from_template(template)
        llm = ChatOpenAI(temperature=0, model_name=self.config.openai.chat_model_name, )
        question_generator = LLMChain(llm=llm, prompt=question_generate_prompt)

        # question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)

        # streaming_llm = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
        # streaming_llm = ChatOpenAI(streaming=True, temperature=0)
        streaming_llm = ChatOpenAI(streaming=True, model_name=self.config.openai.chat_model_name,
                                   callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
        doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=self.prompt, )


        chain = ConversationalRetrievalChain(
            retriever=vectorstore.as_retriever(),
            combine_docs_chain=doc_chain,
            question_generator=question_generator,
            max_tokens_limit=8192,
            return_source_documents=True,
        )
        return chain

    def ask_assistant(self, next_user_prompt):
        print("chat next_user_prompt: ", next_user_prompt)
        chain = self.get_langchain()
        result = chain({"question": next_user_prompt, "chat_history": self.chat_history})
        self.chat_history.append((next_user_prompt, result["answer"]))

        return result

def print_query(query):
    print("question: ", query)
    print('\n')

def print_result(result):
    print('\n')
    print("answer: ", result["answer"])
    print('\n')

def __main__():
    # Initialise database
    config = OmegaConf.load('/Users/liwenw/PycharmProjects/ai/PGx-slco1b1-chatbot/config-1000-50.yaml')
    role = "provider"
    assistant = RetrievalAssistant(config, role)

    query = "For a patient with SLCO1B1 decreased function, what are the CPIC recommendations for simvastatin use?"
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

    query = "What is the impact of SLCO1B1 decreased function for Mevacor dosing? "
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

    query = "What is an optimal dose? "
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

    query = "But my patient has severe Myopathy?"
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

    query = "How do other health factors and conditions impact this?"
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

    query = "What kind of pharmacogenetic test should I order for my patient to reduce SAMS risk?"
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

    query='My patient has significant CVD risk and requires statins to manage her high cholesterol levels. What kind of PGx tests should I order to evaluate SAMS risk, and to appropriately manage her statins?'
    print_query(query)
    result = assistant.ask_assistant(query)
    print_result(result)

if __name__ == '__main__':
    __main__()


