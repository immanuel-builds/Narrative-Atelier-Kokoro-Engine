from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.gemini_provider import GeminiProvider
import os

class InterpretationService:
    def __init__(self):
        # Prefer Groq, fallback to Gemini
        if os.getenv("GROQ_API_KEY"):
            self.provider = GroqProvider()
        else:
            self.provider = GeminiProvider()

    async def interpret(self, text: str, observations: list) -> str:
        prompt = f"""
        As a literary analyst and writing mentor, provide a thoughtful, reflective interpretation of the following prose based on these observations:

        Observations: {observations}

        Prose:
        {text[:2000]}

        Requirements:
        - Be reflective and intelligent.
        - Do NOT be robotic or deterministic.
        - Use language like "This section appears to..." or "There may be an opportunity to..."
        - Focus on the thematic and emotional truth.
        - Keep it brief (under 150 words).
        """

        try:
            return await self.provider.complete(prompt)
        except Exception as e:
            return "The analysis layer is currently reflecting. Please try again in a moment."
