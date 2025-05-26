from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from typing import List, Optional

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embeddings model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# Load vector store
db_directory = "./chroma_db"
vectordb = Chroma(persist_directory=db_directory, embedding_function=embeddings)

# Define request models
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class Response(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
def read_root():
    return {"status": "RAG API is running"}

@app.post("/ask", response_model=Response)
async def ask_question(request: QueryRequest):
    try:
        # Step 1: Get relevant documents from Chroma
        docs = vectordb.similarity_search(request.query, k=request.top_k)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Step 2: Prepare prompt for Ollama
        prompt = f"""Answer the following question based on the provided context. If you cannot answer the question based on the context, say "I don't have enough information to answer this question."

Context:
{context}

Question: {request.query}

Answer:"""
        
        # Step 3: Call Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:12b",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error calling Ollama API")
        
        result = response.json()
        answer = result.get("response", "")
        
        # Return response with sources
        sources = [doc.page_content[:200] + "..." for doc in docs]  # First 200 chars of each source
        
        return Response(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)