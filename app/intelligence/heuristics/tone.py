import re

class ToneAnalyzer:
    STYLE_MARKERS = {
        "restrained": ["perhaps", "seemed", "slight", "minimal", "quiet"],
        "poetic": ["crystalline", "shimmering", "ethereal", "resonance", "echoed"],
        "noir": ["smoke", "shadow", "rain", "pavement", "gritty", "darkness"]
    }

    @staticmethod
    def analyze(text: str) -> list:
        observations = []
        # Detection of tonal drift is complex for MVP, so we look for sudden keyword shifts
        # between first and second half of text.
        words = text.lower().split()
        if len(words) < 200:
            return observations

        mid = len(words) // 2
        half1 = " ".join(words[:mid])
        half2 = " ".join(words[mid:])

        def get_dominant_tone(txt):
            scores = {tone: sum(txt.count(m) for m in markers) for tone, markers in ToneAnalyzer.STYLE_MARKERS.items()}
            return max(scores, key=scores.get) if max(scores.values()) > 2 else None

        tone1 = get_dominant_tone(half1)
        tone2 = get_dominant_tone(half2)

        if tone1 and tone2 and tone1 != tone2:
            observations.append({
                "module": "tone",
                "observation": "Potential tonal shift detected.",
                "severity": "medium",
                "details": f"The early section appears to lean towards '{tone1}', while the later section shifts towards '{tone2}'.",
                "prompt": "Is this transition an intentional evolution of the scene's atmosphere?"
            })

        return observations
