import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Narrative Atelier: Kokoro Engine"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "kokoro-engine-secret-key-12345")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kokoro.db")

settings = Settings()
