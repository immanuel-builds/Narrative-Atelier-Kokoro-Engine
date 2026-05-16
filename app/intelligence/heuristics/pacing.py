import re

class PacingAnalyzer:
    @staticmethod
    def analyze(text: str) -> list:
        observations = []
        paragraphs = [p for p in text.split('\n') if p.strip()]
        if not paragraphs:
            return observations

        # Paragraph density
        avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
        if avg_paragraph_length > 100:
            observations.append({
                "module": "pacing",
                "observation": "High paragraph density detected.",
                "severity": "medium",
                "details": "The average paragraph length is high, which may slow down the reader's immersion. You may consider breaking up long narrative blocks to improve the rhythm.",
                "prompt": "How might shorter paragraphs alter the breathing room of this scene?"
            })

        # Scene length check (rough heuristic)
        word_count = len(text.split())
        if word_count > 3000:
            observations.append({
                "module": "pacing",
                "observation": "Extended scene length.",
                "severity": "low",
                "details": "This section is quite long. Ensure that the narrative tension continues to escalate to avoid stagnation.",
                "prompt": "Is there a natural breaking point where the emotional state of the character shifts?"
            })

        return observations
