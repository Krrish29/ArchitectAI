from app.services.providers.ollama_provider import OllamaProvider


class LLMService:

    def __init__(self):
        self.provider = OllamaProvider()

    def generate(self, prompt: str):
        return self.provider.generate(prompt)