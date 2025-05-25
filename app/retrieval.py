from langchain_community.vectorstores import FAISS
from logger.logging_config import setup_logger

persist_directory = './data/faiss'
logger = setup_logger(name="retrieval", level="DEBUG", log_file="./logs/app.log")

def get_retriever(k, embeddings):
    
    try:
        retriever = FAISS.load_local(
            persist_directory, 
            embeddings, 
            allow_dangerous_deserialization=True
        ).as_retriever(search_type="similarity", search_kwargs={"k": k})
        logger.info(f"FAISS index loaded successfully from {persist_directory}")
    except Exception as e:
        logger.error(f"Error loading FAISS index: {e}")
    
    return retriever