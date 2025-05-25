from langchain.memory import ConversationBufferMemory
from langchain_huggingface import ChatHuggingFace
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
import os
from dotenv import load_dotenv
from retrieval import retriever
from logger.logging_config import setup_logger
load_dotenv()

logger = setup_logger(name="rag_pipeline", level="DEBUG", log_file="./logs/app.log")
model = "meta-llama/Llama-3.2-1B-Instruct"
token =  os.getenv("HUGGINGFACEHUB_API_TOKEN") # Replace with your actual Hugging Face token
llm = ChatHuggingFace(model, token=token)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
persist_directory = 'faiss/'
retriever =  retriever()

prompt = PromptTemplate(
    input_variables=["context", "chat_history", "query"],
    template="""
You are a helpful assistant. Answer the user's question based on the chat history and the provided context. 
If there is no helpful information in the context, say you don't know — do not make up an answer.

Context:
{context}

Chat History:
{chat_history}

User's Question:
{query}

Assistant's Answer:"""
)

qa_chain = ConversationalRetrievalChain(
    llm=llm,
    retriever=retriever,
    memory=memory,
    prompt=prompt
)

def get_response(query):
    try:
        response = qa_chain({
            "question": query,
            "chat_history": memory.chat_memory.messages 
        })
        logger.info(f"Response generated: {response['answer']}")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "An error occurred while processing your request. Please try again later."
    
    return response["answer"]
    