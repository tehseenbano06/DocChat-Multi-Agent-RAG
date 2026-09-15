# DocChat — Multi-Agent RAG Document Q&A System

A local, GitHub-ready implementation of the DocChat architecture from the
provided multi-agent RAG project material.

## Architecture

```text
PDF / DOCX / TXT / MD
        |
        v
     Docling
        |
        v
Header-aware chunking
        |
   +----+----+
   |         |
  BM25    ChromaDB
   |      vectors
   +----+----+
        |
        v
 Hybrid Retriever
        |
        v
 Relevance Checker
    /          \
 out-of-scope  in-scope
    |             |
  reject       Research Agent
                  |
                  v
           Verification Agent
              /        \
        supported    unsupported
             |            |
          final       re-research
```

## Main components

- `document_processor.py` — document conversion and chunking
- `retriever.py` — BM25 + vector hybrid retrieval
- `agents/relevance_checker.py` — scope/relevance decision
- `agents/research_agent.py` — context-grounded answer generation
- `agents/verification_agent.py` — source-grounded verification
- `workflow.py` — LangGraph orchestration and self-correction
- `app.py` — Gradio interface
- `llm.py` — local/provider-independent LLM adapter

## Run locally

### 1. Python

Python 3.11 is recommended.

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Install Ollama

Install Ollama from its official website and then pull a small local model:

```powershell
ollama pull llama3.2:3b
```

Make sure Ollama is running.

### 3. Environment

```powershell
Copy-Item .env.example .env
```

You can leave the default Ollama configuration unchanged.

### 4. Run

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The first run may download the local embedding model.

## Why this version does not require IBM credentials

The original course project uses IBM watsonx.ai inside the Coursera/Skills
Network environment. This repository replaces that provider-specific LLM layer
with a local Ollama backend while retaining the RAG architecture:
hybrid retrieval, multi-agent routing, verification, and self-correction.

No API key is required in the default configuration.

## Optional API mode

`llm.py` supports an OpenAI-compatible endpoint. Configure these variables in
`.env`:

```text
LLM_BACKEND=api
API_BASE_URL=...
API_KEY=...
API_MODEL=...
```

Do not commit `.env`.

## Supported documents

- PDF
- DOCX
- TXT
- Markdown

## Future improvements

- Add source/page citations
- Add retrieval evaluation with Recall@K / MRR
- Add a dedicated query-planning agent for complex multi-hop questions
- Add persistent document collections
- Add streaming responses
- Add automated tests
- Deploy the application
