import redis
from redis.commands.search.query import Query
from create_embedding import create_embedding

INDEX_NAME = "openai"

r = redis.Redis(host="localhost",port=6379)

def query_redis(user_question: str,topK: int) :
   
    question_embedding = create_embedding(user_question)
    print (question_embedding)
    query = Query(f"*=>[KNN {topK} @embedding $vector AS score]").return_fields("content", "score").sort_by("score").paging(0,topK).dialect(2)
    query_params = {
        "vector": question_embedding
    }
    results = r.ft(INDEX_NAME).search(query, query_params).docs
    print(results)

    return results