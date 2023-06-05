from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

text_splitter = RecursiveCharacterTextSplitter(
    separators = "\n",
    chunk_size = 512,
    chunk_overlap  = 128,
    length_function = count_tokens,
)

def generate_chunks(text_data: str) -> List[str]:
    return text_splitter.split_text(text_data)