import re

class DialogueAnalyzer:
    @staticmethod
    def analyze(text: str) -> list:
        observations = []
        # Count dialogue lines (lines starting with quotes)
        dialogue_lines = re.findall(r'["“][^"”]+["”]', text)
        total_words = len(text.split())
        if total_words == 0:
            return observations

        dialogue_word_count = sum(len(line.split()) for line in dialogue_lines)
        ratio = dialogue_word_count / total_words

        if ratio > 0.7:
            observations.append({
                "module": "dialogue",
                "observation": "High dialogue-to-description ratio.",
                "severity": "medium",
                "details": "This section is heavily dominated by dialogue. While conversation is vital, the physical space or sensory details may feel thin.",
                "prompt": "What is happening in the silence between these words?"
            })
        elif ratio < 0.1 and total_words > 500:
            observations.append({
                "module": "dialogue",
                "observation": "Minimal dialogue movement.",
                "severity": "low",
                "details": "The narrative is primarily internal or descriptive. Consider if a character interaction could externalize the current conflict.",
                "prompt": "Could a spoken word challenge the protagonist's current internal state?"
            })

        # Overly long dialogue blocks
        for line in dialogue_lines:
            if len(line.split()) > 150:
                observations.append({
                    "module": "dialogue",
                    "observation": "Extended dialogue block detected.",
                    "severity": "medium",
                    "details": "A character is speaking at length. Large blocks of speech can sometimes feel like 'monologuing' unless the context demands it.",
                    "prompt": "How might the listener react physically to this long explanation?"
                })
                break # Only warn once

        return observations
