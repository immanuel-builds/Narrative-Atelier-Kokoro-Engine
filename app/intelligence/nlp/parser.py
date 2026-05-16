import spacy
from typing import List, Dict

class NLPParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NLPParser, cls).__new__(cls)
            try:
                # Using a small model for efficiency
                cls._instance.nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Fallback if model isn't downloaded
                import os
                os.system("python -m spacy download en_core_web_sm")
                cls._instance.nlp = spacy.load("en_core_web_sm")
        return cls._instance

    def parse(self, text: str):
        return self.nlp(text)

    def get_pos_tags(self, text: str) -> List[Dict]:
        doc = self.parse(text)
        return [{"text": token.text, "pos": token.pos_, "tag": token.tag_} for token in doc]

    def get_entities(self, text: str) -> List[Dict]:
        doc = self.parse(text)
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
