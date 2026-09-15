from config import settings

class LocalLLM:
    """Small adapter so the agents do not depend on a single LLM provider."""

    def __init__(self):
        if settings.llm_backend == "ollama":
            import requests
            self.requests = requests
        elif settings.llm_backend == "api":
            if not settings.api_base_url or not settings.api_key or not settings.api_model:
                raise RuntimeError(
                    "For LLM_BACKEND=api, set API_BASE_URL, API_KEY and API_MODEL."
                )
        else:
            raise ValueError("LLM_BACKEND must be 'ollama' or 'api'.")

    def chat(self, prompt):
        if settings.llm_backend == "ollama":
            response = self.requests.post(
                f"{settings.ollama_url}/api/chat",
                json={
                    "model": settings.ollama_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=180,
            )
            response.raise_for_status()
            return response.json()["message"]["content"].strip()

        from openai import OpenAI
        client = OpenAI(
            base_url=settings.api_base_url,
            api_key=settings.api_key,
        )
        response = client.chat.completions.create(
            model=settings.api_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return response.choices[0].message.content.strip()
