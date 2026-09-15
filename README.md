# DocChat — Multi-Agent RAG Document Q&A System

DocChat is a document question-answering system built using Retrieval-Augmented Generation (RAG) and a multi-agent workflow. It allows users to upload documents and ask questions about their contents, while using hybrid retrieval and answer verification to improve response reliability.

## Overview

Unlike a basic RAG pipeline that directly generates an answer after retrieval, DocChat separates the process into multiple stages:

```text
Documents
    |
    v
Document Processing
    |
    v
Hybrid Retrieval
(BM25 + Vector Search)
    |
    v
Relevance Checker
    |
    +------------------+
    |                  |
Out of Scope        Relevant
    |                  |
    v                  v
 Reject          Research Agent
                       |
                       v
               Verification Agent
                       |
                +------+------+
                |             |
            Supported     Unsupported
                |             |
                v             v
          Final Answer    Re-research
```

## Key Features

### Hybrid Retrieval

DocChat combines two retrieval approaches:

* **BM25** for keyword-based retrieval
* **Vector similarity search** for semantic retrieval
* **Ensemble retrieval** to combine both approaches

This allows the system to retrieve relevant information when the user's wording either matches the document directly or expresses the same idea differently.

### Multi-Agent Architecture

The system uses three specialized agents:

**Relevance Checker**

Determines whether the uploaded documents contain information relevant to the user's question.

Possible classifications:

```text
CAN_ANSWER
PARTIAL
NO_MATCH
```

**Research Agent**

Retrieves relevant document chunks and generates an answer using the retrieved context.

**Verification Agent**

Checks the generated response against the retrieved context and identifies unsupported claims or inconsistencies.

### Self-Correction

Generated answers are not immediately treated as final.

If the Verification Agent determines that an answer is insufficiently supported, the workflow routes the request back to the Research Agent for another retrieval and generation cycle.

```text
Research
   |
   v
Verification
   |
   +---- Supported ------> Final Answer
   |
   +---- Unsupported ----> Research Again
```

This creates a feedback loop for improving the reliability of document-grounded answers.

### Document Processing

DocChat supports:

* PDF
* DOCX
* TXT
* Markdown

PDF and DOCX documents are processed using Docling and converted into structured Markdown before being split into smaller sections for retrieval.

File hashing is used to identify previously processed documents and avoid unnecessary reprocessing.

## Technology Stack

| Category            | Technologies          |
| ------------------- | --------------------- |
| Language            | Python 3.11           |
| LLM                 | Ollama, Llama 3.2 3B  |
| RAG                 | LangChain             |
| Agent Orchestration | LangGraph             |
| Vector Database     | ChromaDB              |
| Keyword Retrieval   | BM25                  |
| Embeddings          | Sentence Transformers |
| Document Processing | Docling               |
| Interface           | Gradio                |

## Project Structure

```text
DocChat-Multi-Agent-RAG/
|
├── agents/
│   ├── __init__.py
│   ├── relevance_checker.py
│   ├── research_agent.py
│   └── verification_agent.py
|
├── examples/
│   └── README.md
|
├── app.py
├── config.py
├── document_processor.py
├── retriever.py
├── llm.py
├── workflow.py
|
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Components

| File                           | Purpose                                                    |
| ------------------------------ | ---------------------------------------------------------- |
| `app.py`                       | Gradio interface, document upload and question handling    |
| `document_processor.py`        | Document conversion, chunking and file hashing             |
| `retriever.py`                 | BM25 and ChromaDB hybrid retrieval                         |
| `llm.py`                       | Interface for the local language model                     |
| `workflow.py`                  | LangGraph workflow and conditional routing                 |
| `agents/relevance_checker.py`  | Determines whether a question is relevant to the documents |
| `agents/research_agent.py`     | Retrieves context and generates the answer                 |
| `agents/verification_agent.py` | Verifies generated answers against retrieved context       |
| `config.py`                    | Application and retrieval configuration                    |

## How the System Works

When a user uploads documents, DocChat first processes them using Docling and creates structured text chunks.

The chunks are indexed using both BM25 and vector-based retrieval.

When a question is submitted:

1. The Relevance Checker determines whether the question can be answered from the uploaded documents.
2. The Hybrid Retriever searches for relevant document chunks.
3. The Research Agent generates an answer using the retrieved context.
4. The Verification Agent checks whether the answer is supported by that context.
5. If the answer is not sufficiently supported, the workflow performs another research cycle.
6. The verified response is returned to the user.

## Example

Suppose a user uploads a research paper and asks:

```text
What methodology was used in the study?
```

The request follows this pipeline:

```text
User Question
      |
      v
Relevance Check
      |
      v
BM25 + Vector Retrieval
      |
      v
Research Agent
      |
      v
Verification Agent
      |
      +------ Supported ------> Answer
      |
      +------ Unsupported ----> Re-research
```

The answer is therefore generated from information retrieved from the uploaded document rather than treating the LLM as the only source of information.

## Why Hybrid Retrieval?

BM25 and vector retrieval solve different retrieval problems.

BM25 is useful when important terms from the question appear directly in the document.

Vector retrieval is useful when the question and document use different wording but have similar meanings.

Combining both methods provides a more flexible retrieval mechanism than relying on only keyword or semantic search.

## Why Verification?

Retrieving relevant context does not guarantee that a generated response will use that context correctly.

DocChat therefore separates **answer generation** from **answer verification**.

The Verification Agent checks whether the generated response is supported by the retrieved information. Unsupported responses can be sent through another research cycle before producing the final response.

## Local LLM Implementation

The original project architecture was implemented in the Coursera/Skills Network environment using IBM watsonx.ai.

This repository uses **Ollama with Llama 3.2 3B** for local inference instead of requiring IBM watsonx credentials.

The core RAG and multi-agent architecture remains:

```text
Document Processing
        |
        v
Hybrid Retrieval
        |
        v
Relevance Checking
        |
        v
Research
        |
        v
Verification
        |
        v
Self-Correction
```

The local setup allows the application to run without an external LLM API key.

## Installation

### Requirements

* Python 3.11
* Git
* Ollama

### 1. Clone the Repository

```powershell
git clone https://github.com/tehseenbano06/DocChat-Multi-Agent-RAG.git
cd DocChat-Multi-Agent-RAG
```

### 2. Create a Virtual Environment

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the Local Model

Install Ollama and download the model:

```powershell
ollama pull llama3.2:3b
```

Make sure Ollama is running before starting the application.

### 5. Configure the Environment

Create the environment file:

```powershell
Copy-Item .env.example .env
```

The default configuration uses Ollama, so no API key is required.

Do not commit `.env` or any API keys to the repository.

### 6. Run the Application

```powershell
python app.py
```

Open the application at:

```text
http://127.0.0.1:5000
```
