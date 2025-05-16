import numpy as np
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from components.embedder import BGEEmbedder
from components.vector_db import FaissVectorDB
from components.llm import ToolCallingChatbot


db = FaissVectorDB()
embedder = BGEEmbedder()

with open("files/articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)
    

def rag(query):
    embedding = embedder.embed_sentence(query)
    embedding = embedding.reshape(1, -1)

    search_result = db.search(query_embedding=embedding, top_k=3)
    
    result = []
    
    for i in search_result:
        target_index = i['index']
        distance = i['distance']
        
        for entry in articles:
            if entry["index"] == target_index:
                entry["distance"] = distance
                result.append(entry)
                
    return result


class QueryRequest(BaseModel):
    query: str
    user_id: str
    
user_chatbots = {}


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def health_check():
    return {"health": "OK"}

@app.post("/ask_llm")
async def ask_llm(request: QueryRequest):
    user_id = request.user_id
    query = request.query

    if user_id not in user_chatbots:
        user_chatbots[user_id] = ToolCallingChatbot()

    chatbot = user_chatbots[user_id]

    try:
        result = chatbot.ask(query, function=rag)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")
