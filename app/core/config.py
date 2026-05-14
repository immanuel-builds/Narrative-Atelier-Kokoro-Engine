import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Narrative Atelier: Kokoro Engine"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "kokoro-engine-secret-key-12345")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kokoro.db")

    # AI API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Default AI Provider
    DEFAULT_AI_PROVIDER: str = os.getenv("DEFAULT_AI_PROVIDER", "groq") # groq or gemini

settings = Settings()
