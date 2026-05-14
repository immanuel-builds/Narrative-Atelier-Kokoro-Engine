from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.integrity_guard import IntegrityGuard
from app.core.config import settings
from app.reliability.fallback_manager import FallbackManager

class CoachingService:
    def __init__(self):
        if settings.DEFAULT_AI_PROVIDER == "gemini":
            self.provider = GeminiProvider(settings.GEMINI_API_KEY)
        else:
            self.provider = GroqProvider(settings.GROQ_API_KEY)

    async def get_critique(self, text: str) -> str:
        if not text.strip():
            return "Please write something first so I can provide guidance."

        system_prompt = (
            f"{IntegrityGuard.get_guard_prompt()}\n\n"
            "Analyze the provided scene and offer editorial guidance on: "
            "1. Pacing\n2. Dialogue quality\n3. Emotional subtext\n4. Scene clarity\n"
            "Focus on constructive, literary advice. Keep it brief and elegant."
        )
        user_prompt = f"Critique the following scene:\n\n{text}"

        return await self.provider.generate_text(system_prompt, user_prompt, temperature=0.5)

    async def explain_technique(self, technique: str) -> str:
        system_prompt = f"{IntegrityGuard.get_guard_prompt()}\n\nExplain the requested narrative technique clearly and concisely."
        user_prompt = f"Explain the technique: {technique}"

        return await self.provider.generate_text(system_prompt, user_prompt, temperature=0.4)
