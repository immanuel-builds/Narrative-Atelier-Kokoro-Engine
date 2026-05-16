import re

class ProtagonistAnalyzer:
    @staticmethod
    def analyze(text: str) -> list:
        observations = []

        # Heuristic for passive protagonist
        # Look for high frequency of passive voice indicators (was/were + ed)
        passive_indicators = len(re.findall(r'\b(was|were)\s+\w+ed\b', text, re.I))
        word_count = len(text.split())

        if word_count > 0:
            passive_density = passive_indicators / (word_count / 100)
            if passive_density > 1.5:
                observations.append({
                    "module": "protagonist",
                    "observation": "Passive protagonist drift detected.",
                    "severity": "medium",
                    "details": "The narrative frequently uses passive constructions which may distance the reader from the protagonist's agency.",
                    "prompt": "How might this scene change if the protagonist initiated more of the actions?"
                })

        # Heuristic for reactive sentence structures
        reactive_words = len(re.findall(r'\b(felt|seemed|realized|saw|heard|noticed)\b', text, re.I))
        if word_count > 0:
            reactive_density = reactive_words / (word_count / 100)
            if reactive_density > 2.0:
                 observations.append({
                    "module": "protagonist",
                    "observation": "Filter word density is high.",
                    "severity": "low",
                    "details": "High use of filter words can sometimes reduce the intimacy of the character's experience.",
                    "prompt": "Could you remove the filter words to place the reader directly in the experience?"
                })

        return observations
