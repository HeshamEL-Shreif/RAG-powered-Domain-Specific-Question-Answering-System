from langchain_community.embeddings  import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from logger.logging_config import setup_logger

logger = setup_logger(name="rag_pipeline", level="DEBUG", log_file="./logs/app.log")




def initiate_pipeline(persist_directory = './data/chroma_langchain_db'):

    model_name_or_path = "meta-llama/Llama-3.2-1B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path)

    text_gen_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=1024
    )

    llm = HuggingFacePipeline(pipeline=text_gen_pipeline)
    logger.info("[INFO] LLM initialized successfully.")
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    logger.info("[INFO] Embeddings initialized successfully.")
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    vector_store = Chroma(
    collection_name="rag_system",
    embedding_function=embeddings,
    persist_directory=persist_directory,
    )
    logger.info("[INFO] Vector store initialized successfully.")

    qa_prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template="""
    You are a knowledgeable and concise AI assistant. Use the context and the chat history to answer the user's question clearly and accurately.

    Guidelines:
    - Only use information from the context and prior conversation (chat history).
    - If the answer is not present in the context, say: "The context does not provide enough information to answer this question."
    - If interpretation is needed, rely strictly on the context and prior exchanges.
    - Be specific, informative, and avoid unnecessary repetition.
    - focus on the question be specific in your answer and try to be concise

    Chat History:
    {chat_history}

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    )
     
    return llm, memory, qa_prompt, vector_store

def format_chat_history(messages):
    formatted = []
    for msg in messages:
        if msg.__class__.__name__ == "HumanMessage":
            formatted.append(f"Human: {msg.content}")
        elif msg.__class__.__name__ == "AIMessage":
            formatted.append(f"AI: {msg.content}")
    return "\n".join(formatted)



def rag(query, llm, qa_prompt, memory, vector_store):
    
    retrieved_docs = vector_store.similarity_search(query)
    logger.info(f"[INFO] Retrieved {len(retrieved_docs)} documents for query: {query}")
    
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    
    chat_history = format_chat_history(memory.chat_memory.messages)
    messages = qa_prompt.invoke({"question": query, "context": docs_content, "chat_history":chat_history})
    logger.info(f"[INFO] Generated messages for query:")
    
    llm = llm.bind(skip_prompt=True)
    response = llm.invoke(messages)
    logger.info(f"[INFO] Response generated for query")
    
    memory.save_context({"input": query}, {"output": response})
    logger.info(f"[INFO] Memory updated with query")
    
    return response
    