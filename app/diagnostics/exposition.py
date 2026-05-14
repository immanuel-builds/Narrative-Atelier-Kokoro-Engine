import re

class ExpositionAnalyzer:
    EXPOSITION_KEYWORDS = ["explained", "realized", "understood", "remembered", "knew", "thought", "knew that", "was because"]

    @staticmethod
    def analyze(text: str) -> list:
        observations = []
        paragraphs = [p for p in text.split('\n') if p.strip()]
        if not paragraphs:
            return observations

        # Detect potential info-dumping (consecutive paragraphs without dialogue and high keyword count)
        exposition_heavy_streak = 0
        max_streak = 0
        for p in paragraphs:
            if not re.search(r'["“]', p):
                keyword_hits = sum(1 for word in ExpositionAnalyzer.EXPOSITION_KEYWORDS if word in p.lower())
                if keyword_hits > 2 or len(p.split()) > 150:
                    exposition_heavy_streak += 1
                else:
                    exposition_heavy_streak = 0
            else:
                exposition_heavy_streak = 0
            max_streak = max(max_streak, exposition_heavy_streak)

        if max_streak >= 3:
            observations.append({
                "module": "exposition",
                "observation": "Potential exposition density detected.",
                "severity": "medium",
                "details": "Extended sections of internal realization or history without sensory action. This may lead to 'telling' rather than 'showing'.",
                "prompt": "Can this information be discovered through an object or a confrontation instead?"
            })

        return observations
