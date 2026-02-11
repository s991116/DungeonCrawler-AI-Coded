"""
Item scaffolding for future inventory and equipment systems.

For now this only defines a minimal Item base class so other parts of
the game can type-hint against it without providing behavior.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    """Base item type (placeholder for future expansion)."""

    name: str
    description: Optional[str] = None

