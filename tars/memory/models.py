from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Memory:
    id: str
    category: str
    key: str
    content: str
    importance: float # 0.0 to 1.0
    created_at: datetime
    updated_at: datetime
    source: str # e.g. "user", "system"
