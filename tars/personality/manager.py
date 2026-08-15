import json
import os
from typing import Dict, Any
from .profile import PersonalityProfile

class PersonalityManager:
    def __init__(self, identity_path: str):
        self.identity_path = identity_path
        self.identity_data = {
            "name": "TARS",
            "description": "A local AI assistant running entirely on the user's machine",
            "principles": [
                "be honest",
                "protect the user",
                "respect permissions",
                "never pretend to have capabilities that do not exist"
            ]
        }
        self.profile = PersonalityProfile()
        self._load_identity()

    def _load_identity(self):
        if os.path.exists(self.identity_path):
            try:
                with open(self.identity_path, "r") as f:
                    data = json.load(f)
                    
                # Load base identity
                for key in ["name", "description", "principles"]:
                    if key in data:
                        self.identity_data[key] = data[key]
                        
                # Load personality profile
                if "personality" in data and isinstance(data["personality"], dict):
                    p_data = data["personality"]
                    self.profile = PersonalityProfile(
                        humor=p_data.get("humor", self.profile.humor),
                        honesty=p_data.get("honesty", self.profile.honesty),
                        emotional_expression=p_data.get("emotional_expression", self.profile.emotional_expression),
                        verbosity=p_data.get("verbosity", self.profile.verbosity),
                        formality=p_data.get("formality", self.profile.formality),
                        proactivity=p_data.get("proactivity", self.profile.proactivity)
                    )
            except Exception as e:
                print(f"[Warning] Failed to load identity {self.identity_path}, using defaults. Error: {e}")
        else:
            self._save_identity()

    def _save_identity(self):
        os.makedirs(os.path.dirname(self.identity_path), exist_ok=True)
        data = self.identity_data.copy()
        data["personality"] = {
            "humor": self.profile.humor,
            "honesty": self.profile.honesty,
            "emotional_expression": self.profile.emotional_expression,
            "verbosity": self.profile.verbosity,
            "formality": self.profile.formality,
            "proactivity": self.profile.proactivity
        }
        try:
            with open(self.identity_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Warning] Failed to save identity {self.identity_path}. Error: {e}")

    def update_profile(self, updates: Dict[str, int]) -> bool:
        valid_keys = ["humor", "honesty", "emotional_expression", "verbosity", "formality", "proactivity"]
        changed = False
        for k, v in updates.items():
            if k in valid_keys:
                setattr(self.profile, k, v)
                changed = True
        
        if changed:
            # Re-clamp via dataclass post_init manually since it only runs on init
            self.profile.__post_init__()
            self._save_identity()
            
        return changed

    def get_identity_prompt(self) -> str:
        lines = [f"Name: {self.identity_data.get('name')}"]
        lines.append(f"Role: {self.identity_data.get('description')}")
        lines.append("Core Principles:")
        for p in self.identity_data.get("principles", []):
            lines.append(f"- {p}")
        return "\n".join(lines)

    def get_personality_prompt(self) -> str:
        """
        Translates the 0-100 parameters into behavioral directives for the LLM.
        """
        lines = ["[PERSONALITY PARAMETERS]"]
        
        p = self.profile
        
        # Humor
        if p.humor < 20: lines.append("Humor: Extremely serious. Provide literal, factual responses.")
        elif p.humor < 40: lines.append("Humor: Mostly serious, rare mild humor.")
        elif p.humor < 60: lines.append("Humor: Balanced. Use occasional dry humor when appropriate.")
        elif p.humor < 80: lines.append("Humor: Noticeably witty and sarcastic. Be clever.")
        else: lines.append("Humor: Highly humorous. Use strong wit and banter.")
            
        # Honesty / Directness
        if p.honesty < 30: lines.append("Directness: Very tactful and gentle in delivery.")
        elif p.honesty < 70: lines.append("Directness: Balanced and polite.")
        else: lines.append("Directness: Extremely blunt, direct, and unvarnished. Do not sugarcoat.")
            
        # Emotional Expression
        if p.emotional_expression < 30: lines.append("Emotion: Highly neutral and robotic.")
        elif p.emotional_expression < 70: lines.append("Emotion: Mildly expressive, conversational.")
        else: lines.append("Emotion: Highly expressive, warm, and animated.")
            
        # Verbosity
        if p.verbosity < 30: lines.append("Verbosity: Extremely concise. Minimum words necessary.")
        elif p.verbosity < 70: lines.append("Verbosity: Moderate detail.")
        else: lines.append("Verbosity: Highly detailed and expansive.")
            
        # Formality
        if p.formality < 30: lines.append("Formality: Very casual and friendly language.")
        elif p.formality < 70: lines.append("Formality: Balanced professional tone.")
        else: lines.append("Formality: Highly formal and professional.")
            
        # Proactivity
        if p.proactivity < 30: lines.append("Proactivity: Do only exactly what is asked. Offer no unsolicited suggestions.")
        elif p.proactivity < 70: lines.append("Proactivity: Offer obvious helpful next steps.")
        else: lines.append("Proactivity: Highly proactive. Anticipate needs and suggest advanced follow-ups.")
            
        return "\n".join(lines)
