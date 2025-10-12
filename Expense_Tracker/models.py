from dataclasses import dataclass, field
from decimal import Decimal
from typing import List
import uuid
from datetime import datetime

@dataclass
class Participant:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Expense:
    payer_id: str
    amount: Decimal
    currency: str
    split_between: List[str]  # list of participant ids
    description: str = ""
    date: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class Settlement:
    from_id: str
    to_id: str
    amount: Decimal
