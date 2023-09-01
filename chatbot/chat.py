# -*- coding:utf-8 -*-
# Created by liwenw at 8/17/23

import os, sys
import streamlit as st
from streamlit_chat import message
from omegaconf import OmegaConf
import argparse

from chatbot import RetrievalAssistant, Message
def parse_args(args):
    parser = argparse.ArgumentParser(description='demo how to use streamlit for ai embeddings to question/answer.')
    parser.add_argument("-y", "--yaml", dest="yamlfile",
                        help="Yaml file for project", metavar="YAML")
    parser.add_argument("-r", "--role", dest="role",
                        help="role(patient/provider) for question/answering", metavar="ROLE")
    return parser.parse_args(args)


args = parse_args(sys.argv[1:])
if args.yamlfile is None:
    os._exit(-1)

yamlfile = args.yamlfile
config = OmegaConf.load(yamlfile)

role = args.role

### CHATBOT APP

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":shark:"
)

st.title('PGx SLCOLB1 Chatbot')
st.subheader("Help us help you learn about PGx SLCOLB1")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input(f"What do you want to know: ", key="input")

if st.button('Submit', key='generationSubmit'):

    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant(config=config, role=role)
        messages = []
    else:
        messages = []

    response = query(prompt)
    # print(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['answer'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
