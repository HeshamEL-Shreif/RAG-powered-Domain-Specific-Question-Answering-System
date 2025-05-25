from logger.logging_config import setup_logger

logger = setup_logger(name="rag_pipeline", level="DEBUG", log_file="./logs/app.log")

def get_response(query, qa_chain):
    try:
        response = qa_chain.invoke({"question": query})
        logger.info(f"Response generated: {response['answer']}")
        logger.debug(f"Full response details: {response}")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "An error occurred while processing your request. Please try again later."
    
    return response["answer"]


