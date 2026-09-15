from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    # Local embedding model; downloaded automatically by sentence-transformers.
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = int(os.getenv("TOP_K", "5"))
    bm25_weight: float = float(os.getenv("BM25_WEIGHT", "0.5"))
    vector_weight: float = float(os.getenv("VECTOR_WEIGHT", "0.5"))
    max_total_size_mb: int = int(os.getenv("MAX_TOTAL_SIZE_MB", "50"))

    # LLM backend:
    # ollama = fully local; api = OpenAI-compatible endpoint.
    llm_backend: str = os.getenv("LLM_BACKEND", "ollama")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    api_base_url: str = os.getenv("API_BASE_URL", "")
    api_key: str = os.getenv("API_KEY", "")
    api_model: str = os.getenv("API_MODEL", "")

    @property
    def max_total_size_bytes(self):
        return self.max_total_size_mb * 1024 * 1024

settings = Settings()
Path("data/chroma").mkdir(parents=True, exist_ok=True)
