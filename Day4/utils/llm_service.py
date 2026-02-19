from abc import ABC, abstractmethod
import os
import time
from typing import Iterator
from dotenv import load_dotenv
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI

load_dotenv()

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
    @abstractmethod
    def generate_stream(self, prompt: str) -> Iterator[str]:
        pass


class GeminiProvider(BaseProvider):
    def __init__(self, model_id="gemini-2.5-pro"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set")

        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text.strip()
    
    def generate_stream(self, prompt: str):
        stream = self.client.models.generate_content_stream(
            model=self.model_id,
            contents=prompt
        )

        for event in stream:
            if event.text:
                for char in event.text:
                    yield char
                    time.sleep(0.01)

class OpenAIProvider(BaseProvider):
    def __init__(self, model_id="gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        self.client = OpenAI(api_key=api_key)
        self.model_id = model_id

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()


class LLMFactory:
    @staticmethod
    def get_provider(provider_type: str) -> BaseProvider:
        if provider_type == "gemini":
            return GeminiProvider()
        if provider_type == "openai":
            return OpenAIProvider()
        raise ValueError(f"Provider {provider_type} not supported.")
    