import httpx
from typing import List, Dict, Any
from app.ai.providers.base_provider import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    async def generate_text(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        full_prompt = f"System Instruction: {system_prompt}\n\nUser: {user_prompt}"
        messages = [{"role": "user", "parts": [{"text": full_prompt}]}]
        return await self.chat_completion(messages, **kwargs)

    async def chat_completion(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        if not self.api_key:
            return "[Gemini API Key not configured]"

        payload = {
            "contents": messages,
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 2048)
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                return f"Gemini Error: {str(e)}"
