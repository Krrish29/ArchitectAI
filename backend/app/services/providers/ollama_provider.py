import ollama
from app.services.providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def generate(self, prompt: str):

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]