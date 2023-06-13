# -*- coding:utf-8 -*-
# Created by liwenw at 6/12/23

from langchain.vectorstores.chroma import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from chromadb.config import Settings
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from omegaconf import OmegaConf
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='demo how to use ai embeddings to chat.')
    parser.add_argument("-y", "--yaml", dest="yamlfile",
                        help="Yaml file for project", metavar="YAML")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.yamlfile is None:
        parser.print_help()
        exit()

    yamlfile = args.yamlfile
    config = OmegaConf.load(yamlfile)

    # Load environment variables
    load_dotenv()

    model = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        # openai.api_key = config.openai.api_key,
        model_name='gpt-4',
        temperature=0.0
    )
    embeddings = OpenAIEmbeddings()

    collection_name = config.chromadb.collection_name
    persist_directory = config.chromadb.persist_directory
    chroma_db_impl = config.chromadb.chroma_db_impl

    vector_store = Chroma(collection_name=collection_name,
                          embedding_function=embeddings,
                          client_settings=Settings(
                              chroma_db_impl=chroma_db_impl,
                              persist_directory=persist_directory
                          ),
                          )

    system_template = """You are AI-powered chatbot designed to provide accurate and up-to-date information related to pharmacogenetics testing results for patients who have undergone testing or providers looking for information regarding their patient's care. You will use the following pieces of context to answer the users question.
    Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
    If you don't know the answer, just say that "I don't know", don't try to make up an answer. Make sure to not to provide medical care or assumptions about treatment, always ensure that the user reaches out to appropriate sources or providers for care plans. Also ensure that you reference other factors that might impact care.
    """
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
        condense_question_prompt=prompt
        # verbose=True,
    )

    chat_history = []

    while True:
        print()
        question = input("Question: ")

        # Get answer
        response = chain({"question": question, "chat_history": chat_history, "summaries": ""})
        answer = response["answer"]
        source = response["source_documents"]
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=answer))

        # Display answer
        print("\nSources:")
        for document in source:
            print(document)
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()