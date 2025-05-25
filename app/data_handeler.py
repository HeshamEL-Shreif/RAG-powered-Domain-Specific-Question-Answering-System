import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from logger.logging_config import setup_logger


logger = setup_logger(name="data_handler", level="DEBUG", log_file="./logs/app.log")

persist_directory = './data/faiss'
os.makedirs(persist_directory, exist_ok=True)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

def load_documents(file_path, embeddings):

    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.endswith('.csv'):
        loader = CSVLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    documents = loader.load()
    split_docs = splitter.split_documents(documents)


    vectorstore = FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)
    vectorstore.add_documents(split_docs)

    vectorstore.save_local(persist_directory)