import re

class SceneMovementAnalyzer:
    @staticmethod
    def analyze(text: str) -> list:
        observations = []

        paragraphs = [p for p in text.split('\n') if p.strip()]
        if not paragraphs:
            return observations

        # Heuristic for scene movement: transition words
        transitions = re.findall(r'\b(then|later|afterward|suddenly|meanwhile|next|soon|finally)\b', text, re.I)

        word_count = len(text.split())
        if word_count > 0:
            transition_density = len(transitions) / (word_count / 100)

            if transition_density < 0.5:
                observations.append({
                    "module": "movement",
                    "observation": "Low scene movement detected.",
                    "severity": "low",
                    "details": "There are few explicit temporal or causal transitions, which might make the scene feel static or circular.",
                    "prompt": "What external event could propel the character toward the next moment?"
                })

        return observations
