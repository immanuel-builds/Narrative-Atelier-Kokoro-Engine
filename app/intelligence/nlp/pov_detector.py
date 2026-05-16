from app.intelligence.nlp.parser import NLPParser

class POVDetector:
    def __init__(self):
        self.parser = NLPParser()

    def detect(self, text: str) -> str:
        doc = self.parser.parse(text)

        first_person_pronouns = {"i", "me", "my", "mine", "we", "us", "our", "ours"}
        second_person_pronouns = {"you", "your", "yours"}
        third_person_pronouns = {"he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"}

        counts = {"first": 0, "second": 0, "third": 0}

        for token in doc:
            lower_text = token.text.lower()
            if lower_text in first_person_pronouns:
                counts["first"] += 1
            elif lower_text in second_person_pronouns:
                counts["second"] += 1
            elif lower_text in third_person_pronouns:
                counts["third"] += 1

        if counts["first"] > counts["third"] and counts["first"] > counts["second"]:
            return "First Person"
        elif counts["second"] > counts["first"] and counts["second"] > counts["third"]:
            return "Second Person"
        else:
            return "Third Person"
