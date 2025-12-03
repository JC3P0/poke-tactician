"""
Type Effectiveness Table - Pokemon Gen 1 Type Matchups

Uses HashTable from CS_311 Assignment 7 for O(1) type effectiveness lookup.

Gen 1 Type Chart:
- Super Effective: 2x damage
- Not Very Effective: 0.5x damage
- No Effect: 0x damage (immune)
- Normal: 1x damage

Gen 1 Quirks:
- Ghost is IMMUNE to Normal/Fighting (but this was bugged and didn't work)
- Psychic has NO WEAKNESS (Ghost/Bug were supposed to be super effective but bugged)
- Ice resists Ice (this changed in later gens)
- Bug is super effective against Poison (changed in Gen 2)
- Poison is super effective against Bug (changed in Gen 2)

This implementation uses the ACTUAL Gen 1 mechanics, bugs and all!

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project - Uses Assignment 7 (Hash Tables)
"""

import sys
import os
from typing import Optional

# Add parent directory to path to import dataStructures
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataStructures.hash_table import HashTable


class TypeEffectiveness:
    """
    Type effectiveness lookup using HashTable (CS_311 Assignment 7).

    Stores all Gen 1 type matchups for O(1) lookup during damage calculation.
    """

    def __init__(self):
        """
        Initialize the type effectiveness table.

        Uses HashTable with initial size of 200 (plenty for ~225 type matchups).
        """
        # HashTable from Assignment 7 - separate chaining implementation
        self._table = HashTable(size=200)

        # Initialize all type matchups
        self._initialize_matchups()

    def _initialize_matchups(self):
        """
        Populate the hash table with all Gen 1 type matchups.

        Key format: "AttackType:DefenseType" (e.g., "Fire:Grass")
        Value: Multiplier (2.0, 0.5, 0.0, or 1.0)
        """

        # Format: (attack_type, defense_type, multiplier)
        matchups = [
            # Normal
            ("Normal", "Rock", 0.5),
            ("Normal", "Ghost", 0.0),  # Gen 1 bug: should be 0, was actually 0

            # Fire
            ("Fire", "Fire", 0.5),
            ("Fire", "Water", 0.5),
            ("Fire", "Grass", 2.0),
            ("Fire", "Ice", 2.0),
            ("Fire", "Bug", 2.0),
            ("Fire", "Rock", 0.5),
            ("Fire", "Dragon", 0.5),

            # Water
            ("Water", "Fire", 2.0),
            ("Water", "Water", 0.5),
            ("Water", "Grass", 0.5),
            ("Water", "Ground", 2.0),
            ("Water", "Rock", 2.0),
            ("Water", "Dragon", 0.5),

            # Electric
            ("Electric", "Water", 2.0),
            ("Electric", "Electric", 0.5),
            ("Electric", "Grass", 0.5),
            ("Electric", "Ground", 0.0),  # Immune
            ("Electric", "Flying", 2.0),
            ("Electric", "Dragon", 0.5),

            # Grass
            ("Grass", "Fire", 0.5),
            ("Grass", "Water", 2.0),
            ("Grass", "Grass", 0.5),
            ("Grass", "Poison", 0.5),
            ("Grass", "Ground", 2.0),
            ("Grass", "Flying", 0.5),
            ("Grass", "Bug", 0.5),
            ("Grass", "Rock", 2.0),
            ("Grass", "Dragon", 0.5),

            # Ice
            ("Ice", "Water", 0.5),
            ("Ice", "Grass", 2.0),
            ("Ice", "Ice", 0.5),  # Gen 1: Ice resists Ice (changed in Gen 2)
            ("Ice", "Ground", 2.0),
            ("Ice", "Flying", 2.0),
            ("Ice", "Dragon", 2.0),

            # Fighting
            ("Fighting", "Normal", 2.0),
            ("Fighting", "Ice", 2.0),
            ("Fighting", "Poison", 0.5),
            ("Fighting", "Flying", 0.5),
            ("Fighting", "Psychic", 0.5),
            ("Fighting", "Bug", 0.5),
            ("Fighting", "Rock", 2.0),
            ("Fighting", "Ghost", 0.0),  # Immune

            # Poison
            ("Poison", "Grass", 2.0),
            ("Poison", "Poison", 0.5),
            ("Poison", "Ground", 0.5),
            ("Poison", "Bug", 2.0),  # Gen 1 only (changed in Gen 2)
            ("Poison", "Rock", 0.5),
            ("Poison", "Ghost", 0.5),

            # Ground
            ("Ground", "Fire", 2.0),
            ("Ground", "Electric", 2.0),
            ("Ground", "Grass", 0.5),
            ("Ground", "Poison", 2.0),
            ("Ground", "Flying", 0.0),  # Immune
            ("Ground", "Bug", 0.5),
            ("Ground", "Rock", 2.0),

            # Flying
            ("Flying", "Electric", 0.5),
            ("Flying", "Grass", 2.0),
            ("Flying", "Fighting", 2.0),
            ("Flying", "Bug", 2.0),
            ("Flying", "Rock", 0.5),

            # Psychic
            ("Psychic", "Fighting", 2.0),
            ("Psychic", "Poison", 2.0),
            ("Psychic", "Psychic", 0.5),
            # Gen 1 bug: Ghost and Bug should be super effective, but they're not

            # Bug
            ("Bug", "Fire", 0.5),
            ("Bug", "Grass", 2.0),
            ("Bug", "Fighting", 0.5),
            ("Bug", "Poison", 2.0),  # Gen 1 only
            ("Bug", "Flying", 0.5),
            ("Bug", "Psychic", 2.0),  # Gen 1 bug: implemented as 0.5x, not 2x
            ("Bug", "Ghost", 0.5),
            ("Bug", "Rock", 0.5),  # Added in Gen 2

            # Rock
            ("Rock", "Fire", 2.0),
            ("Rock", "Ice", 2.0),
            ("Rock", "Fighting", 0.5),
            ("Rock", "Ground", 0.5),
            ("Rock", "Flying", 2.0),
            ("Rock", "Bug", 2.0),

            # Ghost
            ("Ghost", "Normal", 0.0),  # Gen 1: Ghost immune to Normal
            ("Ghost", "Psychic", 0.0),  # Gen 1 bug: should be 2x, was 0x
            ("Ghost", "Ghost", 2.0),

            # Dragon
            ("Dragon", "Dragon", 2.0),
        ]

        # Insert all matchups into hash table
        for attack_type, defense_type, multiplier in matchups:
            key = f"{attack_type}:{defense_type}"
            self._table.insert(key, multiplier)

    def get_multiplier(self, attack_type: str, defense_type: str) -> float:
        """
        Get the type effectiveness multiplier.

        Args:
            attack_type: Type of the attacking move
            defense_type: Type of the defending Pokemon

        Returns:
            Multiplier (2.0, 0.5, 0.0, or 1.0 for neutral)

        Time Complexity: O(1) average case (hash table lookup)
        """
        key = f"{attack_type}:{defense_type}"

        # Look up in hash table (O(1) average)
        multiplier = self._table.get(key)

        # If not found in table, it's neutral (1x)
        if multiplier is None:
            return 1.0

        return multiplier

    def get_multiplier_dual_type(
        self,
        attack_type: str,
        defense_type1: str,
        defense_type2: Optional[str] = None
    ) -> float:
        """
        Get type effectiveness against a Pokemon with 1 or 2 types.

        For dual-type Pokemon, multiply both type matchups.
        Example: Fire vs Water/Ground = 0.5 * 2.0 = 1.0 (neutral)

        Args:
            attack_type: Type of the attacking move
            defense_type1: Primary type of defending Pokemon
            defense_type2: Secondary type (None if single-type)

        Returns:
            Combined multiplier
        """
        multiplier = self.get_multiplier(attack_type, defense_type1)

        if defense_type2 is not None:
            multiplier *= self.get_multiplier(attack_type, defense_type2)

        return multiplier

    def is_super_effective(self, attack_type: str, defense_type: str) -> bool:
        """Check if attack is super effective (>1x)."""
        return self.get_multiplier(attack_type, defense_type) > 1.0

    def is_not_very_effective(self, attack_type: str, defense_type: str) -> bool:
        """Check if attack is not very effective (<1x, but not 0)."""
        multiplier = self.get_multiplier(attack_type, defense_type)
        return 0.0 < multiplier < 1.0

    def is_immune(self, attack_type: str, defense_type: str) -> bool:
        """Check if defending type is immune (0x)."""
        return self.get_multiplier(attack_type, defense_type) == 0.0

    def get_effectiveness_text(self, multiplier: float) -> str:
        """
        Get user-friendly text for effectiveness.

        Args:
            multiplier: Type effectiveness multiplier

        Returns:
            Text like "Super effective!", "Not very effective...", etc.
        """
        if multiplier == 0.0:
            return "It doesn't affect the foe..."
        elif multiplier >= 4.0:
            return "It's super effective! (4x)"
        elif multiplier >= 2.0:
            return "It's super effective!"
        elif multiplier == 1.0:
            return ""  # No message for neutral
        elif multiplier == 0.5:
            return "It's not very effective..."
        elif multiplier <= 0.25:
            return "It's not very effective... (0.25x)"
        else:
            return ""


# Singleton instance for global use
_type_chart = None


def get_type_chart() -> TypeEffectiveness:
    """
    Get the singleton TypeEffectiveness instance.

    Returns:
        Global TypeEffectiveness instance
    """
    global _type_chart
    if _type_chart is None:
        _type_chart = TypeEffectiveness()
    return _type_chart


# For convenient importing
TYPE_CHART = get_type_chart()
