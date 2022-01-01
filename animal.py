from dataclasses import field, dataclass
from typing import List


@dataclass
class Animal:
    name: str
    href: str
    collateral_adjectives: List[str] = field(default_factory=list)
