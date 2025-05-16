# AZ Labor Code Legal Bot (RAG + Tool Use)

This is a legal chatbot built using Retrieval-Augmented Generation (RAG) with tool calling on the **Labor Code of Azerbaijan**.

## Stack Used

- [Together AI](https://www.together.ai/) – `meta-llama/Llama-3.3-70B-Instruct-Turbo` for LLM inference
- Embedding Model – `bge-m3` via `SentenceTransformers`
- Vector Store – `FAISS`
- API Deployment – `FastAPI` for serving the chatbot backend

## Getting Started

1. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source venv/bin/activate
   ```

2. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a .env file in the root directory with the following variable:**

   ```ini
   TOGETHER_API_KEY=your_api_key_here
   ```

4. **Run the app:**

   ```bash
   uvicorn chat:app --reload
   ```

## Notes
- You can find the chunked articles in "files/articles.json".
- This project was developed and tested on a machine with RTX 4090 GPU — ensure sufficient GPU resources for local embedding inference.
- All user chat histories are currently stored in-memory only (non-persistent).
