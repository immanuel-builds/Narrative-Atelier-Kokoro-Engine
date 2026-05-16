class RiskEngine:
    def __init__(self):
        pass

    def analyze_risks(self, observations: list) -> list:
        risks = []

        # Aggregate heuristics into high-level risks
        pacing_issues = [o for o in observations if o['module'] == 'pacing' and o['severity'] == 'medium']
        if len(pacing_issues) > 0:
            risks.append({
                "risk": "Pacing Stagnation",
                "observation": "Reader tension may weaken in this section due to high paragraph density or extended scene length."
            })

        passive_issues = [o for o in observations if o['module'] == 'protagonist']
        if len(passive_issues) > 0:
            risks.append({
                "risk": "Passive Protagonist Drift",
                "observation": "The character may appear reactive rather than active, potentially reducing reader investment."
            })

        return risks
