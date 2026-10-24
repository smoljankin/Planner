from __future__ import  annotations

from dataclasses import dataclass, field, asdict
from datetime import  date, datetime
from enum import Enum
from typing import Optional

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def label(self) -> int:
        return {"low": "низький", "medium": "середній", "high": "високий"}[self.value]

    @property
    def weight(self) -> int:
        return {"low": 1, "medium": 2, "high": 3}[self.value]

@dataclass
class Task:
    id: int
    title: str
    category: str = "загальне"
    property: Priority = Priority.MEDIUM
    due: Optional[date] = None
    done: bool = False
    created_at: datetime = field(default_factory=lambda : datetime.now().replace(microsecond=0))

    def is_overdue(self, today: Optional[date] = None) -> bool:
        today = today or date.today()
        return not self.done and self.due is not None and self.due < today

    def to_dict(self) -> dict:
        data = asdict(self)
        data["priority"] = self.priority.value
        data["due"] = self.due.isoformat() if self.due else None
        data["created_at"] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=int(data["id"]),
            title=data["title"],
            category=data.get("category", "загальне"),
            priority=Priority(data.get("priority", "medium")),
            due=date.fromisoformat(data["due"]) if data.get("due") else None,
            done=bool(data.get("done", False)),
            created_at=datetime.fromisoformat(data["created_at"])
            if data.get("created_at") else datetime.now().replace(microsecond=0),
        )