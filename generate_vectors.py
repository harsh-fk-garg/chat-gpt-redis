import redis
from redis.commands.search.field import TagField, VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import os
import openai
from chunking import generate_chunks
from create_embedding import create_embedding

# set openai api key
openai.api_key = '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'

# define redis client
r = redis.Redis(host="localhost", port=6379)

INDEX_NAME = "openai"                    
DOC_PREFIX = "doc:"                              

def create_index(vector_dimensions: int):

    SCHEMA = [
        TagField("tag"),
        TextField("content"),
        VectorField("embedding", "FLAT", {"TYPE": "FLOAT32", "DIM": vector_dimensions, "DISTANCE_METRIC": "COSINE",}),
    ]
    DEFINITION = IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.HASH)
    
    try:
        # check to see if index exists
        r.ft(INDEX_NAME).info()
        print("Index already exists!")
    except:
        # create Index
        r.ft(INDEX_NAME).create_index(fields=SCHEMA, definition=DEFINITION)
        print("Index created")

# define vector dimensions
VECTOR_DIMENSIONS = 1536

# create the index
create_index(vector_dimensions=VECTOR_DIMENSIONS)

# store the reference files
files = os.listdir('docs')

# get current directory
directory = os.path.dirname(os.path.abspath(__file__))

# loop through the files
for j in range(1,len(files)): 

    file = files[j]
    with open(directory + f"/docs/{file}", 'r') as f:
        text = f.read()
    
    chunks = generate_chunks(text)

    i=0 
    for chunk in chunks: 

        key = f"{file}:chunk-{i}"
        i=i+1

        vector = create_embedding(chunk)

        mapping = {
            "embedding" : vector,
            "content" : chunk,
            "tag" : file
        }
        r.hset(name=key,mapping=mapping)

print("Embeddings generated")