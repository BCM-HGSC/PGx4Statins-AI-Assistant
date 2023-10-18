# -*- coding:utf-8 -*-
# Created by liwenw at 10/16/23


from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import os
import pandas as pd
import ast
import torch
from copy import deepcopy

from chromadb.config import Settings
from omegaconf import OmegaConf
import re
import argparse
def create_parser():
    parser = argparse.ArgumentParser(description='demo how to use ai embeddings to chat.')
    parser.add_argument("-y", "--yaml", dest="yamlfile",
                        help="Yaml file for project", metavar="YAML")
    return parser


def evaluate_conditions(conditions,answer):
    '''
    Ex - condition = [[str1,str2],[str3,str4]]
    evaluates to (str1 and str2) or (str3 and str4)
    '''
    boolean_list = []
    for condition in conditions:
        if len(condition) > 1:
            if all(re.search(re.escape(c), answer, re.IGNORECASE) for c in condition):
                boolean_list.append(True)
            else:
                boolean_list.append(False)
        else:
            if re.search(re.escape(condition[0] ), answer, re.IGNORECASE):
                boolean_list.append(True)
            else:
                boolean_list.append(False)
    result = any(boolean_list)
    return result

import re
def retrieve(db, question, k):
    res_dict = {}
    retrieved_docs = db.similarity_search_with_score(question, k=k)
    for idx, (doc,score) in enumerate(retrieved_docs):
        res_dict[idx+1] = [score,doc.page_content]
    return res_dict
def main():

    parser = create_parser()
    args = parser.parse_args()

    if args.yamlfile is None:
        parser.print_help()
        exit()

    yamlfile = args.yamlfile
    config = OmegaConf.load(yamlfile)
    data_dirs = config.data.directory
    chunk_size = config.parse_pdf.chunk_size
    chunk_overlap = config.parse_pdf.chunk_overlap

    question_file = config.validation_file
    test_questions = pd.read_csv(question_file)
    df_final_summary = test_questions.groupby('category').agg({'question': 'count'}).reset_index()
    df_final_individual_summary = test_questions

    csv_docs = []
    for data_dir in data_dirs:
        print(f"Ingest files at {data_dir}")
        if data_dir.endswith("pdfs"):
            loader = PyPDFDirectoryLoader(data_dir)
            pdf_docs = loader.load()
        elif data_dir.endswith("csvs"):
            for filename in os.listdir(data_dir):
                if filename.endswith(".csv") and os.path.isfile(os.path.join(data_dir, filename)):
                    print(f"Upserting {filename}")
                    csv_loader = CSVLoader(os.path.join(data_dir, filename))
                    pages = csv_loader.load()
                    print(f"Number of pages: {len(pages)}")
                    csv_docs.extend(pages)
        else:
            continue
    docs = pdf_docs + csv_docs
    print(f"Total number of documents: {len(docs)}")
    documents = deepcopy(csv_docs)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    batch_size = config.huggingface.batch_size
    normalize_embeddings = config.huggingface.normalize_embeddings
    print(f"Using device: {device}",
          f"\nBatch size: {batch_size}",
          f"\nNormalize embeddings: {normalize_embeddings}")

    # Create a new collection with the given name and embedding function.
    embed_model = HuggingFaceEmbeddings(
        model_name=config.huggingface.embedding_model_name,
        model_kwargs={'device': device},
        encode_kwargs={'device': device, 'batch_size': batch_size, 'normalize_embeddings': normalize_embeddings}
        # equivalent to cosine sim
    )

    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = text_splitter.split_documents(documents)

    db = FAISS.from_documents(documents,embed_model)

    chat_search_type = 'similarity'
    for k in [5, 10, 20]:
        print(f"chat_search_type: {chat_search_type}")
        print(f"chat_search_k: {k}")

        output_summary = f"output_summary_{chat_search_type}_{k}.csv"
        output_pagecontent = f"output_pagecontent_{chat_search_type}_{k}.txt"
        final_summary = "final_summary.csv"
        output_pagecontent_handler = open(output_pagecontent, "w")

        simscore_dict_final = {}
        evaluation_dict_final = {}

        for q, a in zip(test_questions['question'], test_questions['answer']):
            output_pagecontent_handler.write(f"question: {q}\n")
            # set up  data structure
            simscore_per_question = []
            evaluation_per_question = []

            # retrieve docs from vector store
            retrieved_docs = retrieve(db, q, k)

            output_pagecontent_handler.write(f"retrieved_docs: {docs}\n\n")

            # evaluate conditions on retrieved docs
            conditions = ast.literal_eval(a)
            for key, item in retrieved_docs.items():
                evaluate_response = evaluate_conditions(conditions, item[1])
                simscore_per_question.append(item[0])
                evaluation_per_question.append(evaluate_response)
            simscore_dict_final[q] = simscore_per_question
            evaluation_dict_final[q] = evaluation_per_question
        # create dataframe for evaluation results and write to csv
        name_columns = ['question', 'category']
        num_columns = [i for i in range(0, k)]
        columns = name_columns + num_columns

        df_evaluation = pd.DataFrame(evaluation_dict_final)
        df_evaluation = df_evaluation.T
        df_evaluation = df_evaluation.reset_index().merge(test_questions[['question', 'category']],
                                                          left_on="index", right_on="question")[columns]
        df_evaluation['total_matches'] = df_evaluation[num_columns].astype(int).sum(axis=1)
        df_evaluation['success'] = (df_evaluation['total_matches'] >= 1).astype(int)
        df_final_individual_summary[f"success_{chat_search_type}_{k}"] = df_evaluation['success']

        df_evaluation.to_csv(output_summary)

        output_pagecontent_handler.close()
        df_interm_summary = df_evaluation.groupby('category').agg({'success': 'mean', 'question': 'count'}).reset_index()
        df_final_summary[f"{chat_search_type}_{k}"] = df_interm_summary['success']

    # write summary final results
    df_final_individual_summary.to_csv("final_individual_summary.csv")
    df_final_summary.to_csv(final_summary)
    print(df_final_summary)




if __name__ == "__main__":
    main()



