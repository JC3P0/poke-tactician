"""
Damage Calculator - Pokemon Gen 1 Damage Formula

Implements the authentic Gen 1 damage calculation formula.

Gen 1 Damage Formula:
    Damage = (((2 * Level / 5 + 2) * Power * A / D) / 50 + 2) * Modifiers

Where:
    - Level = Attacker's level
    - Power = Move's base power
    - A = Attack stat (physical) or Special stat (special moves)
    - D = Defense stat (physical) or Special stat (special moves)
    - Modifiers = STAB * Type * Critical * Random

Modifiers:
    - STAB (Same Type Attack Bonus): 1.5 if move type matches attacker, else 1.0
    - Type: Type effectiveness from TypeEffectiveness table (HashTable!)
    - Critical: 2.0 for critical hit, 1.0 otherwise
    - Random: Random variance from 217-255, divided by 255 (85-100% of damage)

Gen 1 Critical Hit Mechanics:
    - Base critical rate = BaseSpeed / 512
    - High critical moves (Slash, Razor Leaf, etc.) = BaseSpeed / 64
    - Focus Energy is BUGGED and reduces crit rate instead of increasing it
    - Crits ignore stat modifiers (not relevant for this project)

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import random
import sys
import os
from typing import Tuple, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pokemon import Pokemon
from models.move import Move
from utils.typeEffectiveness import TYPE_CHART


class DamageCalculator:
    """
    Handles all damage calculations for Gen 1 Pokemon battles.

    Uses the authentic Gen 1 damage formula with all its quirks and bugs.
    """

    @staticmethod
    def calculate_damage(
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        is_critical: Optional[bool] = None,
        random_roll: Optional[int] = None
    ) -> int:
        """
        Calculate damage for an attack.

        Args:
            attacker: Attacking Pokemon
            defender: Defending Pokemon
            move: Move being used
            is_critical: Force critical hit (None = calculate randomly)
            random_roll: Force random variance (217-255, None = random)

        Returns:
            Damage dealt (integer)

        Time Complexity: O(1) - constant time calculation
        Space Complexity: O(1)
        """

        # Status moves deal no damage
        if move.power == 0:
            return 0

        # Get attacker's offensive stat (Attack or Special)
        if move.is_physical:
            attack_stat = attacker.attack
        else:
            attack_stat = attacker.special

        # Get defender's defensive stat (Defense or Special)
        if move.is_physical:
            defense_stat = defender.defense
        else:
            defense_stat = defender.special

        # Determine if critical hit occurs
        if is_critical is None:
            is_critical = DamageCalculator._is_critical_hit(attacker, move)

        # Calculate base damage
        level = attacker.level
        power = move.power

        # Gen 1 formula: (((2 * Level / 5 + 2) * Power * A / D) / 50 + 2)
        base = (2 * level / 5 + 2) * power * attack_stat / defense_stat
        base = int(base / 50) + 2

        # Calculate modifiers
        stab = DamageCalculator._calculate_stab(attacker, move)
        type_effectiveness = DamageCalculator._calculate_type_effectiveness(move, defender)
        critical = 2.0 if is_critical else 1.0

        # Random variance: 217-255 (85-100% of damage)
        if random_roll is None:
            random_roll = random.randint(217, 255)
        random_multiplier = random_roll / 255.0

        # Apply all modifiers
        damage = base * stab * type_effectiveness * critical * random_multiplier

        # Round down and return
        return int(damage)

    @staticmethod
    def calculate_damage_range(
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        is_critical: bool = False
    ) -> Tuple[int, int]:
        """
        Calculate min and max possible damage (with random variance).

        Args:
            attacker: Attacking Pokemon
            defender: Defending Pokemon
            move: Move being used
            is_critical: Whether to calculate for critical hit

        Returns:
            Tuple of (min_damage, max_damage)
        """
        min_damage = DamageCalculator.calculate_damage(
            attacker, defender, move,
            is_critical=is_critical,
            random_roll=217  # Minimum roll
        )

        max_damage = DamageCalculator.calculate_damage(
            attacker, defender, move,
            is_critical=is_critical,
            random_roll=255  # Maximum roll
        )

        return (min_damage, max_damage)

    @staticmethod
    def calculate_average_damage(
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        include_crit_chance: bool = True
    ) -> float:
        """
        Calculate average damage (accounting for random variance and crits).

        Args:
            attacker: Attacking Pokemon
            defender: Defending Pokemon
            move: Move being used
            include_crit_chance: Include critical hit probability in average

        Returns:
            Average damage (float)
        """
        # Average random roll: (217 + 255) / 2 = 236
        avg_random = 236

        if include_crit_chance:
            # Calculate crit rate
            crit_rate = DamageCalculator._get_crit_rate(attacker, move)

            # Calculate damage for both crit and non-crit
            non_crit_damage = DamageCalculator.calculate_damage(
                attacker, defender, move,
                is_critical=False,
                random_roll=avg_random
            )

            crit_damage = DamageCalculator.calculate_damage(
                attacker, defender, move,
                is_critical=True,
                random_roll=avg_random
            )

            # Weighted average
            return non_crit_damage * (1 - crit_rate) + crit_damage * crit_rate
        else:
            # Just average without crits
            return DamageCalculator.calculate_damage(
                attacker, defender, move,
                is_critical=False,
                random_roll=avg_random
            )

    @staticmethod
    def _calculate_stab(attacker: Pokemon, move: Move) -> float:
        """
        Calculate STAB (Same Type Attack Bonus).

        Args:
            attacker: Attacking Pokemon
            move: Move being used

        Returns:
            1.5 if move type matches attacker's type, else 1.0
        """
        if attacker.has_type(move.type):
            return 1.5
        return 1.0

    @staticmethod
    def _calculate_type_effectiveness(move: Move, defender: Pokemon) -> float:
        """
        Calculate type effectiveness using TYPE_CHART (HashTable from Assignment 7).

        Args:
            move: Move being used
            defender: Defending Pokemon

        Returns:
            Type effectiveness multiplier (0.0, 0.5, 1.0, 2.0, or 4.0)

        Time Complexity: O(1) - hash table lookup
        """
        # Use HashTable for O(1) lookup!
        if len(defender.types) == 1:
            return TYPE_CHART.get_multiplier(move.type, defender.types[0])
        else:
            # Dual type: multiply both matchups
            return TYPE_CHART.get_multiplier_dual_type(
                move.type,
                defender.types[0],
                defender.types[1]
            )

    @staticmethod
    def _get_crit_rate(attacker: Pokemon, move: Move) -> float:
        """
        Get critical hit rate for Gen 1.

        Gen 1 crit formula:
        - Normal moves: BaseSpeed / 512
        - High crit moves: BaseSpeed / 64

        Args:
            attacker: Attacking Pokemon
            move: Move being used

        Returns:
            Critical hit probability (0.0 to 1.0)
        """
        base_speed = attacker.base_stats["Speed"]

        # High crit moves (we'll assume none for now, can add later)
        # high_crit_moves = ["Slash", "Razor Leaf", "Crabhammer", "Karate Chop"]
        # if move.name in high_crit_moves:
        #     return min(base_speed / 64.0, 1.0)

        # Normal crit rate
        return min(base_speed / 512.0, 1.0)

    @staticmethod
    def _is_critical_hit(attacker: Pokemon, move: Move) -> bool:
        """
        Determine if attack is a critical hit (random roll).

        Args:
            attacker: Attacking Pokemon
            move: Move being used

        Returns:
            True if critical hit occurs
        """
        crit_rate = DamageCalculator._get_crit_rate(attacker, move)
        return random.random() < crit_rate

    @staticmethod
    def get_damage_description(
        attacker: Pokemon,
        defender: Pokemon,
        move: Move,
        damage: int
    ) -> str:
        """
        Get a text description of the damage calculation.

        Args:
            attacker: Attacking Pokemon
            defender: Defending Pokemon
            move: Move being used
            damage: Damage dealt

        Returns:
            Description string (e.g., "Pikachu's Thunderbolt dealt 45 damage!")
        """
        type_effectiveness = DamageCalculator._calculate_type_effectiveness(move, defender)
        effectiveness_text = TYPE_CHART.get_effectiveness_text(type_effectiveness)

        description = f"{attacker.name}'s {move.name} dealt {damage} damage!"

        if effectiveness_text:
            description += f" {effectiveness_text}"

        return description


# Convenience function for simple damage calculation
def calculate_damage(
    attacker: Pokemon,
    defender: Pokemon,
    move: Move
) -> int:
    """
    Calculate damage (convenience function).

    Args:
        attacker: Attacking Pokemon
        defender: Defending Pokemon
        move: Move being used

    Returns:
        Damage dealt
    """
    return DamageCalculator.calculate_damage(attacker, defender, move)
