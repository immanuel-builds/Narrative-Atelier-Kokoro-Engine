import re

class ReliabilityAnalyzer:
    @staticmethod
    def analyze(text: str) -> dict:
        # Markers of subjectivity/unreliability:
        # - Uncertainty: maybe, perhaps, seemed, must have, likely
        # - Strong bias: hated, loved, always, never (absolute terms)
        # - Contradiction: however, but, yet (when used with internal state)

        uncertainty_markers = ["maybe", "perhaps", "seemed", "appeared", "must have", "likely", "probably", "i think"]
        bias_markers = ["always", "never", "everyone", "nobody", "impossible", "obviously"]

        text_lower = text.lower()
        uncertain_count = sum(text_lower.count(m) for m in uncertainty_markers)
        bias_count = sum(text_lower.count(m) for m in bias_markers)

        score = uncertain_count + bias_count

        if score > 10:
            observation = "High Subjectivity"
            details = "The narrator uses frequent uncertainty and absolute claims, suggesting a heavily filtered perspective."
        elif score > 3:
            observation = "Moderate Subjectivity"
            details = "The perspective includes some emotional filtering and interpretive bias."
        else:
            observation = "Neutral / Reliable"
            details = "The narration appears primarily focused on observational facts with minimal overt bias."

        return {
            "observation": observation,
            "details": details,
            "uncertainty_score": uncertain_count,
            "bias_score": bias_count
        }
