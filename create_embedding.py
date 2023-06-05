import openai
import numpy as np

def create_embedding(text: str): 
    text_embedding = openai.Embedding.create(input=text,model="text-embedding-ada-002")["data"][0]["embedding"]
    text_embedding = np.array(text_embedding).astype(np.float32).tobytes()
    return text_embedding