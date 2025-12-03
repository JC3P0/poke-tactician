"""
Pokemon Class - Pokemon Gen 1 Battle Data

Represents a Pokemon with all relevant Gen 1 battle properties.

Gen 1 Mechanics:
- Stats: HP, Attack, Defense, Speed, Special (unified, not Sp.Atk/Sp.Def)
- DVs (Determinant Values): 0-15 range, similar to later gen IVs
- Stat calculation uses Gen 1 formula
- Pokemon can have 1 or 2 types
- Maximum 4 moves

Used in: Battle simulation, damage calculation, state graph

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

from typing import List, Optional, Dict
from models.move import Move


class Pokemon:
    """
    Represents a Pokemon in Gen 1 battle.

    Attributes:
        name: Pokemon name (e.g., "Pikachu")
        types: List of types (1 or 2 types)
        level: Pokemon level (1-100)
        base_stats: Dictionary of base stats (HP, Attack, Defense, Speed, Special)
        dvs: Dictionary of DVs (0-15 for each stat)
        moves: List of Move objects (max 4)
        current_hp: Current HP (starts at max HP)
        max_hp: Maximum HP (calculated from base + DV + level)
        attack: Attack stat (calculated)
        defense: Defense stat (calculated)
        speed: Speed stat (calculated)
        special: Special stat (calculated) - used for both Sp.Atk and Sp.Def in Gen 1
    """

    def __init__(
        self,
        name: str,
        types: List[str],
        level: int,
        base_stats: Dict[str, int],
        dvs: Optional[Dict[str, int]] = None,
        moves: Optional[List[Move]] = None
    ):
        """
        Create a new Pokemon.

        Args:
            name: Pokemon name
            types: List of 1-2 types (e.g., ["Electric"] or ["Water", "Ice"])
            level: Level (1-100)
            base_stats: Dict with keys: HP, Attack, Defense, Speed, Special
            dvs: Dict with keys: HP, Attack, Defense, Speed, Special (0-15 each)
                 If None, defaults to max DVs (15 for all stats)
            moves: List of Move objects (max 4). If None, empty list.

        Raises:
            ValueError: If invalid types, level, stats, or moves
        """
        self.name = name
        self.types = types
        self.level = level
        self.base_stats = base_stats

        # Validate types
        if len(types) < 1 or len(types) > 2:
            raise ValueError("Pokemon must have 1 or 2 types")

        # Validate level
        if not 1 <= level <= 100:
            raise ValueError("Level must be between 1 and 100")

        # Default DVs to max (15) if not provided
        if dvs is None:
            dvs = {
                "HP": 15,
                "Attack": 15,
                "Defense": 15,
                "Speed": 15,
                "Special": 15
            }
        self.dvs = dvs

        # Validate DVs
        for stat, dv in self.dvs.items():
            if not 0 <= dv <= 15:
                raise ValueError(f"DV for {stat} must be 0-15, got {dv}")

        # Calculate actual stats using Gen 1 formula
        self.max_hp = self._calculate_hp()
        self.attack = self._calculate_stat("Attack")
        self.defense = self._calculate_stat("Defense")
        self.speed = self._calculate_stat("Speed")
        self.special = self._calculate_stat("Special")

        # Current HP starts at max
        self.current_hp = self.max_hp

        # Moves (max 4)
        if moves is None:
            moves = []
        if len(moves) > 4:
            raise ValueError("Pokemon can have at most 4 moves")
        self.moves = moves

    def _calculate_hp(self) -> int:
        """
        Calculate max HP using Gen 1 formula.

        Gen 1 HP Formula:
        HP = ((Base + DV) * 2 + 63) * Level / 100 + Level + 10

        Returns:
            Maximum HP
        """
        base = self.base_stats["HP"]
        dv = self.dvs["HP"]
        level = self.level

        hp = int(((base + dv) * 2 + 63) * level / 100) + level + 10
        return hp

    def _calculate_stat(self, stat_name: str) -> int:
        """
        Calculate a stat (Attack, Defense, Speed, Special) using Gen 1 formula.

        Gen 1 Stat Formula (non-HP):
        Stat = ((Base + DV) * 2 + 63) * Level / 100 + 5

        Args:
            stat_name: Name of stat ("Attack", "Defense", "Speed", "Special")

        Returns:
            Calculated stat value
        """
        base = self.base_stats[stat_name]
        dv = self.dvs[stat_name]
        level = self.level

        stat = int(((base + dv) * 2 + 63) * level / 100) + 5
        return stat

    def take_damage(self, damage: int) -> int:
        """
        Take damage and update current HP.

        Args:
            damage: Amount of damage to take

        Returns:
            Actual damage taken (may be less if HP drops to 0)
        """
        actual_damage = min(damage, self.current_hp)
        self.current_hp -= actual_damage
        return actual_damage

    def heal(self, amount: int) -> int:
        """
        Heal HP.

        Args:
            amount: Amount to heal

        Returns:
            Actual amount healed (may be less if already at max HP)
        """
        actual_heal = min(amount, self.max_hp - self.current_hp)
        self.current_hp += actual_heal
        return actual_heal

    def is_fainted(self) -> bool:
        """Check if this Pokemon has fainted (HP = 0)."""
        return self.current_hp <= 0

    def get_hp_percentage(self) -> float:
        """Get current HP as a percentage of max HP."""
        return (self.current_hp / self.max_hp) * 100 if self.max_hp > 0 else 0

    def has_type(self, type_name: str) -> bool:
        """Check if this Pokemon has a specific type."""
        return type_name in self.types

    def add_move(self, move: Move) -> bool:
        """
        Add a move to this Pokemon.

        Args:
            move: Move to add

        Returns:
            True if added successfully, False if already at 4 moves
        """
        if len(self.moves) >= 4:
            return False
        self.moves.append(move)
        return True

    def remove_move(self, move_name: str) -> bool:
        """
        Remove a move by name.

        Args:
            move_name: Name of move to remove

        Returns:
            True if removed, False if not found
        """
        for i, move in enumerate(self.moves):
            if move.name == move_name:
                self.moves.pop(i)
                return True
        return False

    def get_move(self, move_name: str) -> Optional[Move]:
        """
        Get a move by name.

        Args:
            move_name: Name of move to find

        Returns:
            Move object if found, None otherwise
        """
        for move in self.moves:
            if move.name == move_name:
                return move
        return None

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Pokemon(name='{self.name}', types={self.types}, "
                f"level={self.level}, HP={self.current_hp}/{self.max_hp}, "
                f"moves={len(self.moves)})")

    def __str__(self) -> str:
        """User-friendly string representation."""
        type_str = "/".join(self.types)
        return f"{self.name} (Lv.{self.level} {type_str}) - {self.current_hp}/{self.max_hp} HP"

    def to_dict(self) -> dict:
        """
        Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "types": self.types,
            "level": self.level,
            "base_stats": self.base_stats,
            "dvs": self.dvs,
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "special": self.special,
            "moves": [move.to_dict() for move in self.moves]
        }

    @staticmethod
    def from_dict(data: dict) -> 'Pokemon':
        """
        Create a Pokemon from a dictionary.

        Args:
            data: Dictionary with Pokemon data

        Returns:
            New Pokemon instance
        """
        moves = [Move.from_dict(m) for m in data.get("moves", [])]

        pokemon = Pokemon(
            name=data["name"],
            types=data["types"],
            level=data["level"],
            base_stats=data["base_stats"],
            dvs=data.get("dvs"),
            moves=moves
        )

        # Restore current HP if provided
        if "current_hp" in data:
            pokemon.current_hp = data["current_hp"]

        return pokemon


# Example Gen 1 Pokemon for testing
def create_pikachu(level: int = 50) -> Pokemon:
    """Create a Pikachu for testing."""
    return Pokemon(
        name="Pikachu",
        types=["Electric"],
        level=level,
        base_stats={
            "HP": 35,
            "Attack": 55,
            "Defense": 40,
            "Speed": 90,
            "Special": 50
        },
        moves=[
            Move("Thunderbolt", "Electric", 95, 100, 15),
            Move("Thunder Wave", "Electric", 0, 100, 20),
            Move("Quick Attack", "Normal", 40, 100, 30),
            Move("Thunder", "Electric", 120, 70, 10)
        ]
    )


def create_charizard(level: int = 50) -> Pokemon:
    """Create a Charizard for testing."""
    return Pokemon(
        name="Charizard",
        types=["Fire", "Flying"],
        level=level,
        base_stats={
            "HP": 78,
            "Attack": 84,
            "Defense": 78,
            "Speed": 100,
            "Special": 85
        },
        moves=[
            Move("Flamethrower", "Fire", 95, 100, 15),
            Move("Fire Blast", "Fire", 120, 85, 5),
            Move("Slash", "Normal", 70, 100, 20),
            Move("Fly", "Flying", 70, 95, 15)
        ]
    )


def create_blastoise(level: int = 50) -> Pokemon:
    """Create a Blastoise for testing."""
    return Pokemon(
        name="Blastoise",
        types=["Water"],
        level=level,
        base_stats={
            "HP": 79,
            "Attack": 83,
            "Defense": 100,
            "Speed": 78,
            "Special": 85
        },
        moves=[
            Move("Surf", "Water", 95, 100, 15),
            Move("Hydro Pump", "Water", 120, 80, 5),
            Move("Ice Beam", "Ice", 95, 100, 10),
            Move("Body Slam", "Normal", 85, 100, 15)
        ]
    )
