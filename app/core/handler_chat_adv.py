from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import pandas as pd

CSV_PATH = "app/data/clause.csv"
loader = CSVLoader(file_path=CSV_PATH, source_column="Clause")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. 
{context}
Question: {question}
Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    return_source_documents=True
)

df = pd.read_csv(CSV_PATH)


def ask_questions(question: str):
    result = qa_chain({"query": question})
    query = result['query']
    answer = result['result']
    source_documents = result['source_documents']

    return answer

    # rows = set()
    # for doc in source_documents:
    #     rows.add(doc.metadata['row'])
    # clauses = df.iloc[list(rows)]
    # clauses = clauses[['Clause', 'Clause_Name']]
    # clauses_dict = clauses.to_dict('records')
    # return answer, clauses_dict
