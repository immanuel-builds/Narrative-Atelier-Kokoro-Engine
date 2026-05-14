from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.integrity_guard import IntegrityGuard
from app.core.config import settings

class POVTransformation:
    def __init__(self):
        if settings.DEFAULT_AI_PROVIDER == "gemini":
            self.provider = GeminiProvider(settings.GEMINI_API_KEY)
        else:
            self.provider = GroqProvider(settings.GROQ_API_KEY)

    async def transform(self, text: str, target_pov: str) -> str:
        if not text or not text.strip():
            return ""

        prompt = f"""
As a literary editor and perspective specialist, transform the following scene into {target_pov} point of view.

CRITICAL CONSTRAINTS:
1. Preserve the original meaning and emotional intent.
2. Keep all character actions and plot events exactly as they are.
3. Do not add new scenes, dialogue, or events.
4. Maintain the 'Creative Integrity' of the author's voice.
5. Focus on the psychological and grammatical shifts required for {target_pov}.

Original Scene:
---
{text}
---

Transformed Scene ({target_pov}):
"""
        response = await self.provider.generate_text(
            system_prompt="You are a literary editor specializing in narrative perspective.",
            user_prompt=prompt,
            temperature=0.4
        )
        # Handle potential API failures or empty responses
        if "API Key not configured" in response:
             return f"[AI Transformation Unavailable] {response}"

        return response.strip()
