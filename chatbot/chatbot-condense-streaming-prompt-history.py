# -*- coding:utf-8 -*-
# Created by liwenw at 8/25/23

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
import argparse

from templates import system_provider_template, human_provider_template, system_patient_template, human_patient_template
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


# def create_parser():
#     parser = argparse.ArgumentParser(description='demo how to use ai embeddings to question/answer.')
#     parser.add_argument("-y", "--yaml", dest="yamlfile",
#                         help="Yaml file for project", metavar="YAML")
#     parser.add_argument("-r", "--role", dest="role",
#                         help="role(patient/provider) for question/answering", metavar="ROLE")
#     return parser
#
# # yamlfile = "/Users/liwenw/PycharmProjects/ai/PGx-slco1b1-chatbot/config-1000-50.yaml"
# # config = OmegaConf.load(yamlfile)
#
# parser = create_parser()
# args = parser.parse_args()
#
# if args.yamlfile is None:
#     parser.print_help()
#     exit()

role = 'provider'
yamlfile = '/Users/liwenw/PycharmProjects/ai/PGx-slco1b1-chatbot/config-1000-50.yaml'

# role = args.role
# yamlfile = args.yamlfile
config = OmegaConf.load(yamlfile)

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
prompt = ChatPromptTemplate.from_messages(messages)

print("####################### prompt ###############################")
print(prompt)
print("##############################################################")


embeddings = OpenAIEmbeddings()

collection_name = config.chromadb.collection_name
persist_directory = config.chromadb.persist_directory
chroma_db_impl = config.chromadb.chroma_db_impl

vectorstore = Chroma(collection_name=collection_name,
                      embedding_function=embeddings,
                      client_settings=Settings(
                          chroma_db_impl=chroma_db_impl,
                          persist_directory=persist_directory
                      ),
                      )

llm = ChatOpenAI(temperature=0, model_name=config.openai.chat_model_name,)

streaming_llm = ChatOpenAI(streaming=True, model_name=config.openai.chat_model_name, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=prompt, )

template = (
    "Combine the chat history and follow up question into "
    "a standalone question. Chat History: {chat_history}"
    "Follow up question: {question}"
)
from langchain.prompts import PromptTemplate
question_generate_prompt = PromptTemplate.from_template(template)
question_generator = LLMChain(llm=llm, prompt=question_generate_prompt)

# question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)

chain = ConversationalRetrievalChain(
    retriever=vectorstore.as_retriever(),
    combine_docs_chain=doc_chain,
    question_generator=question_generator,
    max_tokens_limit=8192,
    return_source_documents=True,
)

questions = [
    "My patient takes fluvastatin for managing his cholesterol. Will a SLCO1B1 increased function affect his medication in any way?",
    "This patient is also a CYP2C9 poor metabolizer",
    "But  does the CYP2C9 phenotype also impact fluvastatin?",
    "What does SLCOB1 increased function mean for my patient’s fluvastatin dosage?",
]

chat_history = []
for question in questions:
    print("question: ", question)
    print('\n')
    result = chain({"question": question, "chat_history": chat_history})
    #print(result)
    print('\n')
    chat_history = [(question, result["answer"])]

# chat_history = []
# query = "For a patient with SLCO1B1 decreased function, what are the CPIC recommendations for simvastatin use?"
# print("query: ", query)
# print('\n')
# result = chain({"question": query, "chat_history": chat_history})
# print(result)
# print('\n')
# # print(result["answer"])
# chat_history = [(query, result["answer"])]
# # exit()
#
# query = "What is the impact of SLCO1B1 decreased function for Mevacor dosing? "
# result = chain({"question": query, "chat_history": chat_history})
# print("query: ", query)
# print('\n')
# print(result)
# # print(result["answer"])
# print('\n')
#
# chat_history.append((query, result["answer"]))
# query = "What is an optimal dose? "
# print("query: ", query)
# print('\n')
# result = chain({"question": query, "chat_history": chat_history})
#
# print(result)
# # print(result["answer"])
# print('\n')
# chat_history.append((query, result["answer"]))
#
# query = "But my patient has severe Myopathy?"
# print("query: ", query)
# print('\n')
# result = chain({"question": query, "chat_history": chat_history})
# print(result)
# # print(result["answer"])
# print('\n')
# chat_history.append((query, result["answer"]))
#
# query = "How do other health factors and conditions impact this?"
# print("query: ", query)
# print('\n')
# result = chain({"question": query, "chat_history": chat_history})
# print(result)
# # print(result["answer"])
# print('\n')
# chat_history.append((query, result["answer"]))
#
# query = "What kind of pharmacogenetic test should I order for my patient to reduce SAMS risk?"
# print("query: ", query)
# print('\n')
# result = chain({"question": query, "chat_history": chat_history})
# print(result)
# print('\n')
# # print(result["answer"])
#
# chat_history.append((query, result["answer"]))
# query='My patient has significant CVD risk and requires statins to manage her high cholesterol levels. What kind of PGx tests should I order to evaluate SAMS risk, and to appropriately manage her statins?'
# print("query: ", query)
# print('\n')
# result = chain({"question": query, "chat_history": chat_history})
# print(result)
# print('\n')
# # print(result["answer"])
# chat_history.append((query, result["answer"]))
# # chat_history.pop(0)




