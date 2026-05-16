import random

class ReflectionEngine:
    def __init__(self):
        self.generic_prompts = [
            "What emotional truth changes in this scene?",
            "Is the protagonist choosing or reacting?",
            "What tension remains unresolved by the end of this section?",
            "How does the setting reflect the internal state of the character?",
            "If this scene were removed, what would be lost to the reader?"
        ]

    def get_prompts(self, observations: list) -> list:
        # Mix generic and observation-based prompts
        prompts = [o['prompt'] for o in observations if 'prompt' in o]

        if len(prompts) < 3:
            prompts.extend(random.sample(self.generic_prompts, 3 - len(prompts)))

        return prompts[:3]
