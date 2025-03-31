# RAG-Powered Research Assistant

This is a **Retrieval-Augmented Generation (RAG)** based chatbot that allows users to upload documents and ask questions based on the document content. It uses **ChromaDB** for vector search, **FastAPI** for the backend, and a **React-based frontend** with streaming chat responses.

## Features
- Upload `.txt`, `.pdf`, `.docx` files and process them for retrieval.
- Ask questions about uploaded documents.
- Uses **DeepSeek API** for generating AI-powered responses.
- Real-time streaming responses with markdown rendering.
- Full-stack implementation with **FastAPI backend** and **React frontend**.

## Tech Stack
- **Backend:** FastAPI, ChromaDB, OpenAI API (DeepSeek)
- **Frontend:** React, Tailwind CSS, Markdown rendering
- **Database:** ChromaDB (for vector search)
- **Deployment:** Render, Vercel, or VPS

## Getting Started

### 1. Backend Setup

#### **Prerequisites:**
- Python 3.10+
- Virtual environment (optional but recommended)
- ChromaDB installed

#### **Installation**
```bash
# Clone the repository
git clone https://github.com/johngitahi/rag-researcher.git
cd rag-researcher/backend

# Create a virtual environment
python -m venv venv
```source venv/bin/activate```  # On Windows, use ```venv\\Scripts\\activate```

# Install dependencies
```pip install -r requirements.txt```

# run the app
```uvicorn main:app```

Then run the frontend with ```npm run dev```
