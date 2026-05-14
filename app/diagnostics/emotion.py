class EmotionAnalyzer:
    EMOTION_PATTERNS = {
        "grief": ["sadness", "tears", "loss", "mourning", "pain", "empty", "hollow", "grief"],
        "anger": ["shouted", "rage", "glared", "fist", "angry", "furious", "heated"],
        "fear": ["trembled", "scared", "fear", "darkness", "shadow", "panic", "breathless"]
    }

    @staticmethod
    def analyze(text: str) -> list:
        observations = []
        text_lower = text.lower()

        repeated_emotions = []
        for emotion, keywords in EmotionAnalyzer.EMOTION_PATTERNS.items():
            hits = sum(text_lower.count(word) for word in keywords)
            if hits > 8: # Arbitrary threshold for MVP
                repeated_emotions.append(emotion)

        if repeated_emotions:
            observations.append({
                "module": "emotion",
                "observation": f"Recurring emotional texture: {', '.join(repeated_emotions)}.",
                "severity": "low",
                "details": "The emotional frequency in this section is high. While consistency is good, repeated beats can sometimes lead to emotional fatigue for the reader.",
                "prompt": "Is there a contrasting emotion that could heighten the impact of this primary feeling?"
            })

        return observations
