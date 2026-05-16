from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class ToneClassifier:
    def __init__(self):
        # A very simple pre-trained mock setup for the MVP
        # In a real app, this would be a loaded model file
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = LogisticRegression()

        # Mock training data
        X_train = [
            "The dark shadows loomed over the decaying manor.", # Melancholy/Gothic
            "She laughed as the sun danced on the blue waves.", # Joyful
            "He spoke with a cold, precise clinical detachment.", # Analytical/Cold
            "The battle raged with fire and blood everywhere."   # Intense/Action
        ]
        y_train = ["Melancholy", "Joyful", "Analytical", "Intense"]

        self.vectorizer.fit(X_train)
        X_vec = self.vectorizer.transform(X_train)
        self.classifier.fit(X_vec, y_train)

    def classify(self, text: str) -> str:
        if not text.strip():
            return "Neutral"
        X_vec = self.vectorizer.transform([text])
        return self.classifier.predict(X_vec)[0]
