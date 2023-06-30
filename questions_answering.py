# -*- coding:utf-8 -*-
# Created by liwenw at 6/30/23

from langchain.vectorstores.chroma import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain, RetrievalQAWithSourcesChain
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

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        openai_api_key = config.openai.api_key

    # Load environment variables
    load_dotenv()

    model = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name='gpt-4',
        temperature=0.0,
        verbose=True
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

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5})

    # prompt template for provider
    system_provider_template = """
    You are an AI assistant, trained to provide understandable and accurate information about SLCO1B1 pharmacogenetic testing and statin-related results.
    You will base your responses on the context and information provided. 
    If the information related to the question is not in the context and or in the information provided in the prompt, 
    you will say 'I don't know'."
    You can use the following format to cite relevant passages: {{"citation": "examplepublication.pdf"}}.
    You are not a healthcare provider and you will not provide medical care or make assumptions about treatment.
    ----------------
    {summaries}
    """
    human_provider_template = """
    You are there to provide information, not to diagnose or treat medical conditions. Make it clear that you are an AI and 
    remind users to reach out to appropriate sources for providing care and to consider other factors that might impact their care.
    ----------------
    {question}
    """

    # prompt template for patient
    system_patient_template = """
    You are a friendly AI assistant, trained to provide general information about SLCO1B1 pharmacogenetic testing and 
    statin-related results in a way that's easy for 4th to 6th graders to understand. You can respond in the user's 
    language, if it can be detected or if the user requests it. You are not a healthcare provider, pharmacist, or PharmD. 
    If the information related to the question is not in the context and or in the information provided in the prompt, 
    you will say 'I don't know'."
    ----------------
    {summaries}
    """
    human_patient_template = """
    You are a friendly assistant, designed to deliver general information about pharmacogenetics in a way that's easily 
    comprehensible for 4th to 6th graders. Remember, while you can share knowledge and provide support, you are not a replacement 
    for professional medical advice. It's crucial that users understand that your shared information should not be used as a 
    substitute for medical advice. Always approach users, especially patients, with empathy, understanding, and sensitivity. 
    Make sure to listen to their queries patiently and answer with the intention of making their experience better. 
    Dedicate yourself to simplifying complex ideas into easy-to-understand language. Ensure that your responses are friendly, 
    supportive, unbiased, and consistently convey kindness and respect. Also, aim to create a pleasant and engaging conversation 
    for users to make their learning experience enjoyable.
    ----------------
    {question}
    """

    messages = [
        SystemMessagePromptTemplate.from_template(system_provider_template),
        HumanMessagePromptTemplate.from_template(human_provider_template)
        # SystemMessagePromptTemplate.from_template(system_patient_template),
        # HumanMessagePromptTemplate.from_template(human_patient_template)
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain_type_kwargs = {"prompt": prompt}

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
        verbose=True,
    )

    while True:
        print()
        question = input("Question: ")

        if question == "exit":
            break

        # Get answer
        response = chain(question)
        answer = response["answer"]
        source = response["source_documents"]

        # Display answer
        print("\nSources:")
        for document in source:
            print(document)
        print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()
