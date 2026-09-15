from llm import LocalLLM

class VerificationAgent:
    def __init__(self):
        self.llm = LocalLLM()

    def verify(self, answer, context):
        prompt = f"""
You are a verification agent.

Compare the proposed answer against the supplied source context.

Return EXACTLY:
SUPPORTED: YES or NO
ISSUES: <brief explanation>

An answer is supported only when its factual claims are supported by the context.

PROPOSED ANSWER:
{answer}

SOURCE CONTEXT:
{context}
"""
        raw = self.llm.chat(prompt)
        supported = "YES" if "SUPPORTED: YES" in raw.upper() else "NO"
        return {
            "supported": supported,
            "raw": raw,
        }
