from app.diagnostics.pacing import PacingAnalyzer
from app.diagnostics.dialogue import DialogueAnalyzer
from app.diagnostics.exposition import ExpositionAnalyzer
from app.diagnostics.emotion import EmotionAnalyzer
from app.diagnostics.tone import ToneAnalyzer
from app.diagnostics.protagonist import ProtagonistAnalyzer

class DiagnosticsEngine:
    def __init__(self):
        self.analyzers = [
            PacingAnalyzer,
            DialogueAnalyzer,
            ExpositionAnalyzer,
            EmotionAnalyzer,
            ToneAnalyzer,
            ProtagonistAnalyzer
        ]

    async def run_analysis(self, text: str) -> list:
        all_observations = []
        if not text.strip():
            return all_observations

        for analyzer in self.analyzers:
            try:
                results = analyzer.analyze(text)
                all_observations.extend(results)
            except Exception as e:
                print(f"Error in analyzer {analyzer.__name__}: {str(e)}")

        return all_observations
