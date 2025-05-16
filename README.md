# AZ Labor Code Legal Bot (RAG + Tool Use)

This is a legal chatbot built using Retrieval-Augmented Generation (RAG) with tool calling on the **Labor Code of Azerbaijan**.

## Stack Used

- [Together AI](https://www.together.ai/) – `meta-llama/Llama-3.3-70B-Instruct-Turbo` for LLM inference
- Embedding Model – `bge-m3` via `SentenceTransformers`
- Vector Store – `FAISS`
- API Deployment – `FastAPI` for serving the chatbot backend

## Getting Started

**Create an .env file in the root directory with the following variable:**

   ```ini
   TOGETHER_API_KEY=your_api_key_here
   ```

### Running with Docker

**Build the Docker image and start the service:**

   ```bash
   sudo docker-compose build
   sudo docker-compose up
   ```

Note: During the first startup, the embedder model (bge-m3) will be downloaded. This may take some time.

### Running Locally (Without Docker)

1. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source venv/bin/activate
   ```

2. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   python3 -m main.run
   ```

## Notes
- Chunked legal articles are stored in: files/articles.json
- The embedder model runs locally on CPU
- All user chat histories are currently stored in-memory only (non-persistent).
