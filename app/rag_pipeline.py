from langchain_community.embeddings  import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from app.retrieval import get_retriever
import os
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from logger.logging_config import setup_logger

logger = setup_logger(name="rag_pipeline", level="DEBUG", log_file="./logs/app.log")

persist_directory = './data/faiss'

def initialize_faiss(embeddings):
    
    dummy_docs = [
        Document(page_content="LangChain makes it easy to build LLM-powered applications."),
    ]

    logger.info("[INFO] Initializing dummy embeddings...")

    vectorstore = FAISS.from_documents(dummy_docs, embeddings)

    os.makedirs(persist_directory, exist_ok=True)
    vectorstore.save_local(persist_directory)
    logger.info(f"[SUCCESS] Dummy FAISS index created at: {persist_directory}")
    


def initiate_models():

    model_name_or_path = "meta-llama/Llama-3.2-1B-Instruct"
    

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
    
    question_rewrite_prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template="""
        Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.

        Chat History:
        {chat_history}

        Follow-up Question:
        {input}

        Standalone question:"""
    )
    
    qa_prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template="""
        You are a helpful assistant. Answer the user's question based on the chat history and the provided context.
        If there is no helpful information in the context, say you don't know — do not make up an answer.

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

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=base_retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    
    return qa_chain