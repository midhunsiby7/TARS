from dataclasses import dataclass

def clamp(val, min_val=0, max_val=100):
    try:
        return max(min_val, min(max_val, int(val)))
    except (ValueError, TypeError):
        return 50 # Safe fallback

@dataclass
class PersonalityProfile:
    humor: int = 70
    honesty: int = 85  # directness
    emotional_expression: int = 40
    verbosity: int = 55
    formality: int = 35
    proactivity: int = 70

    def __post_init__(self):
        self.humor = clamp(self.humor)
        self.honesty = clamp(self.honesty)
        self.emotional_expression = clamp(self.emotional_expression)
        self.verbosity = clamp(self.verbosity)
        self.formality = clamp(self.formality)
        self.proactivity = clamp(self.proactivity)
