import os
from langchain.document_loaders import PyPDFLoader, TextLoader, CSVLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from logger.logging_config import setup_logger

logger = setup_logger(name="data_handler", level="DEBUG", log_file="./logs/app.log")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
persist_directory = 'faiss/'

def load_documents(file_path):

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
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    split_docs = splitter.split_documents(documents)

    if os.path.exists(os.path.join(persist_directory, "index.faiss")):
        
        logger.info("Existing FAISS index found. Loading and updating")
        vectorstore = FAISS.load_local(persist_directory, embeddings)
        vectorstore.add_documents(split_docs)
    else:
        logger.info("Creating new FAISS index")
        vectorstore = FAISS.from_documents(split_docs, embeddings)

    vectorstore.save_local(persist_directory)