from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_text(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass
