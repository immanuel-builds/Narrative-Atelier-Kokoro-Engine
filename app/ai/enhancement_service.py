from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.integrity_guard import IntegrityGuard
from app.core.config import settings

class EnhancementService:
    def __init__(self):
        if settings.DEFAULT_AI_PROVIDER == "gemini":
            self.provider = GeminiProvider(settings.GEMINI_API_KEY)
        else:
            self.provider = GroqProvider(settings.GROQ_API_KEY)

    def get_system_prompt(self, enhancement_type: str) -> str:
        base = IntegrityGuard.get_guard_prompt()
        prompts = {
            "tone": "Enhance the tone of the provided prose while preserving meaning and voice. Type: {mode}.",
            "description": "Enhance the sensory details and emotional texture of the provided description without adding major new plot points.",
            "style": "Transform the writing style while preserving the core narrative events and character intent. Goal: {mode}.",
        }
        return f"{base}\n\n{prompts.get(enhancement_type, 'Refine the prose for better flow and clarity.')}"

    async def enhance(self, text: str, enhancement_type: str, mode: str = "balanced") -> str:
        if not IntegrityGuard.check_request(text):
            return "Integrity Violation: I cannot generate full stories or plots. I am here to enhance your existing prose."

        system_prompt = self.get_system_prompt(enhancement_type).replace("{mode}", mode)
        user_prompt = f"Enhance the following text:\n\n{text}"

        return await self.provider.generate_text(system_prompt, user_prompt, temperature=0.6)
