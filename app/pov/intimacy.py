import re

class IntimacyAnalyzer:
    @staticmethod
    def analyze(text: str) -> dict:
        # Heuristics for intimacy:
        # - Internal thought verbs (thought, felt, realized, wondered)
        # - Sensory details (smell, touch, sound)
        # - Sentence length (shorter sentences can mean high immediacy/tension)

        internal_verbs = ["thought", "felt", "realized", "wondered", "knew", "remembered", "imagined", "wished"]
        sensory_words = ["smell", "taste", "heard", "sound", "rough", "smooth", "bright", "dark", "bitter", "sweet"]

        text_lower = text.lower()
        internal_count = sum(text_lower.count(v) for v in internal_verbs)
        sensory_count = sum(text_lower.count(s) for s in sensory_words)

        words = text.split()
        if not words:
            return {"level": "neutral", "score": 0}

        ratio = (internal_count + sensory_count) / len(words)

        if ratio > 0.05:
            level = "High Intimacy"
            description = "The narration is deeply embedded in the character's internal and sensory world."
        elif ratio > 0.02:
            level = "Moderate Intimacy"
            description = "A balance between external action and internal reflection."
        else:
            level = "Observational"
            description = "The narrative maintains a degree of distance, focusing more on external behavior."

        return {
            "level": level,
            "score": round(ratio * 100, 2),
            "description": description,
            "internal_markers": internal_count,
            "sensory_markers": sensory_count
        }
