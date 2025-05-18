from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from mock_ai import generate_mock_response
import redis
import pymongo
from elasticsearch import Elasticsearch
import time

app = FastAPI()

r = redis.Redis(host="localhost", port = 6379)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chat_db"]
es= Elasticsearch("http://localhost:9200")

class Message(BaseModel):
    user: str
    content: str

@app.post("/ask")
def ask_question(msg: Message):
    cache_key = f"{msg.user}:{msg.content}"
    cached = r.get(cache_key)

    if cached:
        response = cached.decode("utf-8")
    else:
        response = generate_mock_response(msg.content)
        r.set(cache_key, response, ex=3600)

    db.messages.insert_one({
        "user": msg.user,
        "content": msg.content,
        "response": response,
        "timestamp": time.time()
    })

    es.index(index="chatlogs", document={
        "user": msg.user,
        "message": msg.content,
        "response": response,
        "timestamp": time.time()
    })

    return {"response": response}