from typing import Any, List, Dict
import openai

openai.api_key = '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'

def apply_prompt_template(question: str) -> str:
    prompt = f"""
        By considering above input from me, answer the question: {question}
    """
    return prompt

def call_chatgpt_api(user_question: str, chunks: List[str]) -> Dict[str, Any]:

    # Send a request to the GPT-3 API
    messages = list(
        map(lambda chunk: {
            "role": "user",
            "content": chunk
        }, chunks))
    question = apply_prompt_template(user_question)
    messages.append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )
    
    return response