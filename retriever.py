from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from config import settings

class RetrieverBuilder:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )

    def build(self, documents):
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory="data/chroma",
        )

        bm25 = BM25Retriever.from_documents(documents)
        bm25.k = settings.top_k

        vector = vector_store.as_retriever(
            search_kwargs={"k": settings.top_k}
        )

        return EnsembleRetriever(
            retrievers=[bm25, vector],
            weights=[settings.bm25_weight, settings.vector_weight],
        )
