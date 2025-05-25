from langchain_community.embeddings  import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from app.retrieval import get_retriever
import os
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from logger.logging_config import setup_logger
from app.data_handeler import load_documents

logger = setup_logger(name="rag_pipeline", level="DEBUG", log_file="./logs/app.log")

persist_directory = './data/faiss'

def initialize_faiss(embeddings):
    
    if len(os.listdir('./data/upload')) > 0:
        for file in os.listdir('./data/upload'):
            file_path = os.path.join('./data/upload', file)
            if os.path.isfile(file_path):
                logger.info(f"[INFO] Loading documents from: {file_path}")
                load_documents(file_path, embeddings)
                logger.info(f"[SUCCESS] Documents loaded from: {file_path}")
    else:
        dummy_docs = [
            Document(page_content="This is a dummy document for testing purposes. It contains no real data but serves as a placeholder.", metadata={"source": "dummy"}),
        ]

        logger.info("[INFO] Initializing dummy embeddings...")

        vectorstore = FAISS.from_documents(dummy_docs, embeddings)

        os.makedirs(persist_directory, exist_ok=True)
        vectorstore.save_local(persist_directory)
        logger.info(f"[SUCCESS] Dummy FAISS index created at: {persist_directory}")
    


def initiate_models():

    model_name_or_path = "llama-3.2-1b-instruct"

    

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path)
    

    text_gen_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
    )
    
    llm = HuggingFacePipeline(pipeline=text_gen_pipeline)
    
    
    chat = llm  
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    qa_prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template="""
        You are a helpful assistant. Use the context and chat history to answer the user's question.

        - If the user greets (e.g., says "hi", "hello"), respond with a short friendly message and do not over-explain.
        - If there is no helpful information in the context, say you don't know and do not make up an answer.
        - If the user asks a question that is not related to the context, say you don't know and do not make up an answer.
        - If the user asks a question that is related to the context, provide a concise and accurate answer based on the context.
        - just answer the question without any additional information or explanations.
        - If the user asks for a summary, provide a brief summary of the context.

        Context:
        {context}

        Chat History:
        {chat_history}

        User's Question:
        {question}

        Assistant's Answer:"""
    )
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    initialize_faiss(embeddings)
    
    logger.info("[INFO] Models initialized successfully.")
    
    return embeddings, chat, memory, qa_prompt
    
    

def get_pipeline(embeddings, chat, memory, qa_prompt):
    
    base_retriever = get_retriever(5, embeddings)
    logger.info("[INFO] Base retriever initialized.")

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=base_retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    logger.info("[INFO] ConversationalRetrievalChain created successfully.")
    
    return qa_chain