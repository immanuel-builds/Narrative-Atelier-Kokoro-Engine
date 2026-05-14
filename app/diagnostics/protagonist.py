class ProtagonistAnalyzer:
    PASSIVE_VERBS = ["was", "were", "been", "seemed", "appeared", "felt like", "stood", "waited", "watched", "observed"]

    @staticmethod
    def analyze(text: str) -> list:
        observations = []
        words = text.lower().split()
        if not words:
            return observations

        # Detect high frequency of passive/reactive verbs
        passive_hits = sum(1 for word in words if word in ProtagonistAnalyzer.PASSIVE_VERBS)
        ratio = passive_hits / len(words)

        if ratio > 0.15: # High threshold for MVP
            observations.append({
                "module": "protagonist",
                "observation": "Potential protagonist passivity.",
                "severity": "medium",
                "details": "A high frequency of observational or reactive verbs detected. If the protagonist is primarily watching or waiting, the narrative movement may stall.",
                "prompt": "What is the most immediate physical action the protagonist can take to challenge their situation?"
            })

        return observations
