import os
import sys

class FallbackManager:
    @staticmethod
    def is_online() -> bool:
        # Simple check for connectivity to a reliable host
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    @staticmethod
    def get_ai_fallback_message(error: str) -> str:
        if "API Key not configured" in error:
            return "[AI Unavailable] API Key not configured. Please check your settings."
        if not FallbackManager.is_online():
            return "[Offline] AI services require an internet connection. Your local manuscript tools remain active."
        return f"[AI Error] A connection issue occurred. Your text is safe. ({error})"
