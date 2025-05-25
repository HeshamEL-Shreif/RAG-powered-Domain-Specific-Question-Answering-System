from langchain.vectorstores import FAISS
from data_handeler import embeddings, persist_directory

def retrieve( k=5):
    
    retriever = FAISS.load_local(persist_directory, embeddings).as_retriever(search_type="similarity", search_kwargs={"k": k})
    
    return retriever