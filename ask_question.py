from typing import Any, List, Dict
import logging
from query_database import query_redis
from generate_response import call_chatgpt_api

def ask(user_question: str):

    # Get relevant chunks from database.
    chunks_response = query_redis(user_question,3)
    chunks = []

    if chunks_response:
        print(f"Found {chunks_response.total} results:")
        for i,chunk in enumerate(chunks_response):
            chunks.append(chunk.content)
    else:
        print("No results found")
    
    logging.info("User's questions: %s", user_question)
    logging.info("Retrieved chunks: %s", chunks)
    
    # Generate response using relevent chunks
    response = call_chatgpt_api(user_question, chunks)
    logging.info("Response: %s", response)
    
    return response["choices"][0]["message"]["content"]

question = input("Ask your doubt: ")
solution = ask(question)
print("Solution:\n")
print(solution)