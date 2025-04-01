from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import chromadb
import os
import asyncio
import pdfplumber
from docx import Document
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specifies allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

api_key = os.getenv("DEEPSEEK_API_KEY")

# OpenAI client (DeepSeek API)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

class ChatRequest(BaseModel):
    query: str

def extract_text_from_file(file: UploadFile):
    try:
        if file.filename.endswith(".pdf"):
            with pdfplumber.open(file.file) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif file.filename.endswith(".docx") or file.filename.endswith(".doc"):
            doc = Document(file.file)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            text = file.file.read().decode("utf-8")
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    text = extract_text_from_file(file)
    collection.add(documents=[text], ids=[file.filename])
    return {"message": "File uploaded and indexed successfully."}

@app.post("/chat")
async def chat(request: ChatRequest):
    query = request.query
    query_embedding = embedding_model.encode([query]).tolist()
    search_results = collection.query(query_embeddings=query_embedding, n_results=3)
    retrieved_texts = [doc for doc in search_results["documents"][0]] if search_results["documents"] else []
    context = "\n".join(retrieved_texts)
    prompt = f"""
    Context:
    {context}
    \nUser Query: {query}
    \nAnswer:
    """
    
    async def stream_response():
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in response:
            yield chunk.choices[0].delta.content
            await asyncio.sleep(0.05)
    
    return StreamingResponse(stream_response(), media_type="text/event-stream")

