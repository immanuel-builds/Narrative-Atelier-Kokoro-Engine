from app.intelligence.heuristics.pacing import PacingAnalyzer
from app.intelligence.heuristics.dialogue import DialogueAnalyzer
from app.intelligence.heuristics.exposition import ExpositionAnalyzer
from app.intelligence.heuristics.emotion import EmotionAnalyzer
from app.intelligence.heuristics.tone import ToneAnalyzer
from app.intelligence.heuristics.protagonist import ProtagonistAnalyzer
from app.intelligence.heuristics.movement import SceneMovementAnalyzer

from app.intelligence.nlp.pov_detector import POVDetector
from app.intelligence.ml.tone_classifier import ToneClassifier

class AnalysisEngine:
    def __init__(self):
        self.heuristics = [
            PacingAnalyzer,
            DialogueAnalyzer,
            ExpositionAnalyzer,
            EmotionAnalyzer,
            ToneAnalyzer,
            ProtagonistAnalyzer,
            SceneMovementAnalyzer
        ]
        self.pov_detector = POVDetector()
        self.tone_classifier = ToneClassifier()

    async def run_full_analysis(self, text: str) -> dict:
        observations = []
        if not text.strip():
            return {"observations": [], "pov": "Unknown", "tone": "Neutral"}

        for analyzer in self.heuristics:
            try:
                results = analyzer.analyze(text)
                observations.extend(results)
            except Exception as e:
                print(f"Error in analyzer {analyzer.__name__}: {str(e)}")

        pov = self.pov_detector.detect(text)
        tone = self.tone_classifier.classify(text)

        return {
            "observations": observations,
            "pov": pov,
            "tone": tone
        }
