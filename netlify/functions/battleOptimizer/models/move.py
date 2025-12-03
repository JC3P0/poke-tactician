"""
Move Class - Pokemon Gen 1 Move Data

Represents a Pokemon move with all relevant Gen 1 properties.

In Gen 1:
- Physical/Special is determined by TYPE, not individual moves
- Physical types: Normal, Fighting, Flying, Poison, Ground, Rock, Bug, Ghost
- Special types: Fire, Water, Grass, Electric, Psychic, Ice, Dragon

Used in: Damage Calculator, Greedy Algorithm (heap-based move selection)

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

from typing import Optional


class Move:
    """
    Represents a Pokemon move in Gen 1.

    Attributes:
        name: Name of the move (e.g., "Thunderbolt")
        type: Type of the move (e.g., "Electric")
        power: Base power of the move (0 for status moves)
        accuracy: Accuracy as a percentage (0-100, None for moves that never miss)
        pp: Power Points - how many times the move can be used
        is_physical: True if physical, False if special (determined by type)
    """

    # Gen 1 Physical types (use Attack/Defense stats)
    PHYSICAL_TYPES = {
        "Normal", "Fighting", "Flying", "Poison",
        "Ground", "Rock", "Bug", "Ghost"
    }

    # Gen 1 Special types (use Special stat for both offense and defense)
    SPECIAL_TYPES = {
        "Fire", "Water", "Grass", "Electric",
        "Psychic", "Ice", "Dragon"
    }

    def __init__(
        self,
        name: str,
        move_type: str,
        power: int,
        accuracy: Optional[int] = 100,
        pp: int = 10
    ):
        """
        Create a new Move.

        Args:
            name: Move name
            move_type: Type (must be valid Gen 1 type)
            power: Base power (0 for status moves)
            accuracy: Accuracy percentage (None for always-hit moves like Swift)
            pp: Power points (default 10)

        Raises:
            ValueError: If type is not a valid Gen 1 type
        """
        self.name = name
        self.type = move_type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.current_pp = pp  # Track remaining PP

        # Validate type
        if move_type not in (Move.PHYSICAL_TYPES | Move.SPECIAL_TYPES):
            raise ValueError(f"Invalid type: {move_type}")

        # Determine if physical or special based on type
        self.is_physical = move_type in Move.PHYSICAL_TYPES

    def use(self) -> bool:
        """
        Use this move (decrement PP).

        Returns:
            True if move was used successfully, False if out of PP
        """
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        return False

    def restore_pp(self, amount: int = None):
        """
        Restore PP (e.g., after using an Ether).

        Args:
            amount: Amount to restore (default: restore to max)
        """
        if amount is None:
            self.current_pp = self.pp
        else:
            self.current_pp = min(self.current_pp + amount, self.pp)

    def is_usable(self) -> bool:
        """Check if this move has PP remaining."""
        return self.current_pp > 0

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Move(name='{self.name}', type='{self.type}', "
                f"power={self.power}, accuracy={self.accuracy}, "
                f"pp={self.current_pp}/{self.pp})")

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.name} ({self.type}, {self.power} power)"

    def to_dict(self) -> dict:
        """
        Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the move
        """
        return {
            "name": self.name,
            "type": self.type,
            "power": self.power,
            "accuracy": self.accuracy,
            "pp": self.pp,
            "current_pp": self.current_pp,
            "is_physical": self.is_physical
        }

    @staticmethod
    def from_dict(data: dict) -> 'Move':
        """
        Create a Move from a dictionary.

        Args:
            data: Dictionary with move data

        Returns:
            New Move instance
        """
        move = Move(
            name=data["name"],
            move_type=data["type"],
            power=data["power"],
            accuracy=data.get("accuracy", 100),
            pp=data.get("pp", 10)
        )
        move.current_pp = data.get("current_pp", move.pp)
        return move


# Common Gen 1 moves for testing and examples
COMMON_MOVES = {
    # Normal type
    "Tackle": Move("Tackle", "Normal", 40, 100, 35),
    "Body Slam": Move("Body Slam", "Normal", 85, 100, 15),
    "Hyper Beam": Move("Hyper Beam", "Normal", 150, 90, 5),

    # Water type
    "Water Gun": Move("Water Gun", "Water", 40, 100, 25),
    "Surf": Move("Surf", "Water", 95, 100, 15),
    "Hydro Pump": Move("Hydro Pump", "Water", 120, 80, 5),

    # Electric type
    "Thunder Shock": Move("Thunder Shock", "Electric", 40, 100, 30),
    "Thunderbolt": Move("Thunderbolt", "Electric", 95, 100, 15),
    "Thunder": Move("Thunder", "Electric", 120, 70, 10),

    # Fire type
    "Ember": Move("Ember", "Fire", 40, 100, 25),
    "Flamethrower": Move("Flamethrower", "Fire", 95, 100, 15),
    "Fire Blast": Move("Fire Blast", "Fire", 120, 85, 5),

    # Grass type
    "Vine Whip": Move("Vine Whip", "Grass", 35, 100, 10),
    "Razor Leaf": Move("Razor Leaf", "Grass", 55, 95, 25),
    "Solar Beam": Move("Solar Beam", "Grass", 120, 100, 10),

    # Psychic type
    "Confusion": Move("Confusion", "Psychic", 50, 100, 25),
    "Psychic": Move("Psychic", "Psychic", 90, 100, 10),

    # Ice type
    "Ice Beam": Move("Ice Beam", "Ice", 95, 100, 10),
    "Blizzard": Move("Blizzard", "Ice", 120, 90, 5),
}
