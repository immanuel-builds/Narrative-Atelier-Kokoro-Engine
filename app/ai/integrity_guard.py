import re

class IntegrityGuard:
    BLOCK_KEYWORDS = [
        "write my novel", "generate full story", "create chapter",
        "invent character", "lore generation", "world building for me",
        "generate plot", "write ending", "write beginning"
    ]

    @staticmethod
    def check_request(text: str) -> bool:
        """Returns True if the request is allowed, False if it violates integrity."""
        text_lower = text.lower()
        for keyword in IntegrityGuard.BLOCK_KEYWORDS:
            if keyword in text_lower:
                return False

        # Rule: If length of requested generation seems like a full chapter (very loose check)
        if len(text_lower.split()) < 5: # Too short to be a valid enhancement request?
             pass

        return True

    @staticmethod
    def get_guard_prompt() -> str:
        return (
            "You are a literary editor and writing coach. "
            "You MUST NEVER generate full stories, plots, characters, or lore. "
            "Your role is exclusively to enhance existing prose, provide critique, "
            "and teach writing techniques. If a user asks you to write for them "
            "rather than enhance for them, politely redirect them to refinement and coaching."
        )
