from llm import LocalLLM

class RelevanceChecker:
    def __init__(self):
        self.llm = LocalLLM()

    def check(self, question, retriever):
        docs = retriever.invoke(question)
        if not docs:
            return "NO_MATCH"

        context = "\n\n".join(d.page_content for d in docs[:5])
        prompt = f"""
Classify whether the question can be answered using the document context.

Return ONLY one label:
CAN_ANSWER
PARTIAL
NO_MATCH

CAN_ANSWER: the context contains enough information.
PARTIAL: the topic is present but important information may be missing.
NO_MATCH: the context is unrelated.

Question:
{question}

Context:
{context}
"""
        result = self.llm.chat(prompt).upper().strip()
        return result if result in {"CAN_ANSWER", "PARTIAL", "NO_MATCH"} else "NO_MATCH"
