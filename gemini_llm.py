# Gemini LLM integration for LangChain
# This file provides a GeminiLLM class for use with LangChain's LLM interface.

from langchain_core.language_models.llms import LLM
from pydantic import Field
import requests

class GeminiLLM(LLM):
    api_key: str = Field(..., exclude=True)
    model: str = "gemini-2.5-flash-preview-05-20"
    temperature: float = 0.0

    @property
    def _llm_type(self):
        return "google_gemini"

    def _call(self, prompt, stop=None, run_manager=None, **kwargs):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": self.temperature}
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return str(result)
