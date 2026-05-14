import re

class POVDetection:
    @staticmethod
    def detect(text: str) -> dict:
        if not text or not text.strip():
            return {"pov": "unknown", "confidence": 0, "indicators": []}

        paragraphs = [p for p in text.split('\n') if p.strip()]

        # Heuristics for pronouns
        # First Person: I, me, my, mine, we, us, our
        # Second Person: you, your, yours
        # Third Person: he, she, they, it, him, her, them, his, hers, theirs

        first_person_patterns = [r'\bI\b', r'\bme\b', r'\bmy\b', r'\bmine\b', r'\bwe\b', r'\bus\b', r'\bour\b']
        second_person_patterns = [r'\byou\b', r'\byour\b', r'\byours\b']
        third_person_patterns = [r'\bhe\b', r'\bshe\b', r'\bthey\b', r'\bhim\b', r'\bher\b', r'\bthem\b', r'\bhis\b', r'\bhers\b', r'\btheirs\b']

        first_count = sum(len(re.findall(p, text, re.I)) for p in first_person_patterns)
        second_count = sum(len(re.findall(p, text, re.I)) for p in second_person_patterns)
        third_count = sum(len(re.findall(p, text, re.I)) for p in third_person_patterns)

        total = first_count + second_count + third_count

        if total == 0:
            return {"pov": "third", "confidence": 0.5, "explanation": "Minimal pronouns detected. Defaulting to third person."}

        # Weighted scores
        scores = {
            "first": first_count / total,
            "second": second_count / total,
            "third": third_count / total
        }

        detected = max(scores, key=scores.get)
        confidence = scores[detected]

        # Refine Third Person (Omniscient vs Limited) - Rough heuristic
        # Omniscient often switches between different characters' internalities
        # (Very difficult with pure regex, but we can look for many proper names + internal markers)

        if detected == "third":
            # If multiple character names are used with internal verbs (thought, felt, realized)
            # across different paragraphs, it might be omniscient.
            pov_type = "third_limited"
            if confidence > 0.9:
                pov_type = "third_limited"
        else:
            pov_type = detected

        return {
            "pov": pov_type,
            "confidence": round(confidence, 2),
            "distribution": {k: round(v, 2) for k, v in scores.items()},
            "explanation": f"Based on pronoun distribution (First: {first_count}, Second: {second_count}, Third: {third_count})."
        }
