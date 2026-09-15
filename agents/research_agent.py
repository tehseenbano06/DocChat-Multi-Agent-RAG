from llm import LocalLLM

class ResearchAgent:
    def __init__(self):
        self.llm = LocalLLM()

    def generate(self, question, retriever):
        docs = retriever.invoke(question)
        context = "\n\n".join(
            f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}"
            for d in docs
        )

        prompt = f"""
You are the research agent in a document-grounded RAG system.

Answer the question using ONLY the supplied context.
Do not invent facts.
If the context does not contain an answer, explicitly say so.
Keep the answer concise but complete.

Question:
{question}

Context:
{context}
"""
        return {
            "answer": self.llm.chat(prompt),
            "context": context,
        }
