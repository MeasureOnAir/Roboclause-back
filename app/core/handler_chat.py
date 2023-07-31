from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import CSVLoader
from langchain.llms import OpenAI

# from langchain.text_splitter import CharacterTextSplitter

# Load the clauses documents
# with open('app/data/clause-text.txt') as f:
#     clauses_text = f.read()

loader = CSVLoader(file_path="app/data/clause.csv", source_column="clause_id")


# split the clauses into documents
# texts = clauses_text.split("\n")
# text_splitter = CharacterTextSplitter()
# docs = text_splitter.create_documents(texts)
docs = loader.load()

# load the question answering chain
chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")


def get_answer(prompt: str):
    """
    Use the loaded question answering chain to answer the question
    :param prompt: User question
    :return: Answer to the question
    Example Question:
    What is the responsibility of the Contractor in setting out all works?
    """
    # run the chain with the loaded documents and the question
    response = chain.run(input_documents=docs, question=prompt)
    print(response)
    return response
