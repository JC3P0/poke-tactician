"""
BattleState Class - Pokemon Gen 1 Battle State

Represents the complete state of a Pokemon battle at any point in time.

Used as:
- Nodes in the battle state graph (CS_311 Assignment 8 - Graph Traversal)
- Keys in the DP memoization table (CS_311 Assignment 7 - Hash Tables)
- States for Dijkstra's algorithm (CS_311 Assignment 9 - Shortest Path)

A BattleState is a snapshot of:
- Both teams (6 Pokemon each, with current HP)
- Which Pokemon are currently active
- Turn counter

BattleState objects must be hashable for use in HashTable memoization.

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

from typing import List, Optional, Tuple
import copy
import sys
import os
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pokemon import Pokemon
from models.move import Move


class BattleState:
    """
    Represents a complete battle state.

    This class is used as:
    - Graph nodes (Assignment 8) - each state is a vertex
    - Hash keys (Assignment 7) - for DP memoization
    - Dijkstra nodes (Assignment 9) - for pathfinding

    Attributes:
        player_team: List of 6 Pokemon (player's team)
        opponent_team: List of 6 Pokemon (opponent's team)
        player_active: Index of active player Pokemon (0-5)
        opponent_active: Index of active opponent Pokemon (0-5)
        turn: Turn counter
    """

    def __init__(
        self,
        player_team: List[Pokemon],
        opponent_team: List[Pokemon],
        player_active: int = 0,
        opponent_active: int = 0,
        turn: int = 0
    ):
        """
        Create a new BattleState.

        Args:
            player_team: List of player's Pokemon (max 6)
            opponent_team: List of opponent's Pokemon (max 6)
            player_active: Index of active player Pokemon
            opponent_active: Index of active opponent Pokemon
            turn: Current turn number

        Raises:
            ValueError: If teams are invalid
        """
        if len(player_team) > 6 or len(player_team) == 0:
            raise ValueError("Player team must have 1-6 Pokemon")
        if len(opponent_team) > 6 or len(opponent_team) == 0:
            raise ValueError("Opponent team must have 1-6 Pokemon")

        self.player_team = player_team
        self.opponent_team = opponent_team
        self.player_active = player_active
        self.opponent_active = opponent_active
        self.turn = turn

    def get_active_player_pokemon(self) -> Pokemon:
        """Get the currently active player Pokemon."""
        return self.player_team[self.player_active]

    def get_active_opponent_pokemon(self) -> Pokemon:
        """Get the currently active opponent Pokemon."""
        return self.opponent_team[self.opponent_active]

    def is_battle_over(self) -> bool:
        """
        Check if the battle is over (one side has all Pokemon fainted).

        Returns:
            True if battle is over
        """
        player_alive = any(not p.is_fainted() for p in self.player_team)
        opponent_alive = any(not p.is_fainted() for p in self.opponent_team)

        return not player_alive or not opponent_alive

    def player_won(self) -> bool:
        """Check if player won (all opponent Pokemon fainted)."""
        return all(p.is_fainted() for p in self.opponent_team)

    def opponent_won(self) -> bool:
        """Check if opponent won (all player Pokemon fainted)."""
        return all(p.is_fainted() for p in self.player_team)

    def get_alive_pokemon_count(self, is_player: bool) -> int:
        """
        Count alive Pokemon on a team.

        Args:
            is_player: True for player team, False for opponent

        Returns:
            Number of alive Pokemon
        """
        team = self.player_team if is_player else self.opponent_team
        return sum(1 for p in team if not p.is_fainted())

    def hash_key(self) -> str:
        """
        Generate a hash key for this state.

        This key is used for:
        - HashTable memoization in DP algorithm (Assignment 7)
        - State deduplication in graph search (Assignment 8)

        The hash includes:
        - Current HP of all Pokemon
        - Active Pokemon indices
        - Turn number (optional, can be removed for more cache hits)

        Returns:
            String hash key uniquely identifying this state

        Time Complexity: O(n) where n is number of Pokemon
        """
        # Format: "P:hp1,hp2,hp3|O:hp1,hp2,hp3|PA:idx|OA:idx|T:turn"
        player_hps = ",".join(str(p.current_hp) for p in self.player_team)
        opponent_hps = ",".join(str(p.current_hp) for p in self.opponent_team)

        key = (f"P:{player_hps}|O:{opponent_hps}|"
               f"PA:{self.player_active}|OA:{self.opponent_active}|"
               f"T:{self.turn}")

        return key

    def __hash__(self) -> int:
        """Python hash function (for use in sets/dicts)."""
        return hash(self.hash_key())

    def __eq__(self, other) -> bool:
        """Equality comparison based on hash key."""
        if not isinstance(other, BattleState):
            return False
        return self.hash_key() == other.hash_key()

    def copy(self) -> 'BattleState':
        """
        Create a deep copy of this state.

        Important for generating successor states without modifying original.

        Returns:
            New BattleState with copied Pokemon
        """
        # Deep copy all Pokemon
        player_team_copy = [copy.deepcopy(p) for p in self.player_team]
        opponent_team_copy = [copy.deepcopy(p) for p in self.opponent_team]

        return BattleState(
            player_team=player_team_copy,
            opponent_team=opponent_team_copy,
            player_active=self.player_active,
            opponent_active=self.opponent_active,
            turn=self.turn
        )

    def generate_successor_states(
        self,
        include_switches: bool = False
    ) -> List[Tuple['BattleState', Move, int]]:
        """
        Generate all possible successor states from this state.

        This is used for:
        - Building the battle state graph (Assignment 8)
        - Exploring states in BFS/DFS (Assignment 8)
        - Finding optimal paths with Dijkstra (Assignment 9)

        Args:
            include_switches: Whether to include Pokemon switches as actions

        Returns:
            List of tuples: (successor_state, move_used, damage_dealt)
            Note: Auto-switching handles Pokemon changes automatically

        Time Complexity: O(m) where m is number of moves (usually 4)
        """
        successors = []

        if self.is_battle_over():
            return successors  # No successors if battle is over

        active_player = self.get_active_player_pokemon()
        active_opponent = self.get_active_opponent_pokemon()

        # Generate successors for each usable move
        for move in active_player.moves:
            if not move.is_usable():
                continue  # Skip moves with 0 PP

            # Create a copy of the state
            next_state = self.copy()

            # Get the Pokemon in the new state
            attacker = next_state.get_active_player_pokemon()
            defender = next_state.get_active_opponent_pokemon()

            # Import here to avoid circular dependency
            from utils.damageCalculator import DamageCalculator

            # Calculate damage
            damage = DamageCalculator.calculate_damage(attacker, defender, move)

            # OPTIMIZATION: Skip immune moves (0 damage) to reduce graph size
            if damage == 0:
                continue  # Don't explore this branch

            # Apply damage
            defender.take_damage(damage)

            # Use the move (decrement PP)
            next_state.get_active_player_pokemon().get_move(move.name).use()

            # If opponent Pokemon fainted, switch to next available
            if defender.is_fainted():
                next_state._auto_switch_opponent()

            # OPPONENT COUNTERATTACK (Gen 1: both attack in same turn based on Speed)
            # Only counter if battle isn't over and opponent is still alive
            elif not next_state.is_battle_over():
                opponent_attacker = next_state.get_active_opponent_pokemon()
                player_defender = next_state.get_active_player_pokemon()

                # Gen 1 Trainer AI: Priority-based move selection with type effectiveness
                if opponent_attacker.moves:
                    usable_moves = [m for m in opponent_attacker.moves if m.is_usable()]
                    if usable_moves:
                        # Calculate priority for each move (Gen 1 AI algorithm)
                        from utils.typeEffectiveness import TYPE_CHART

                        move_priorities = []
                        for m in usable_moves:
                            priority = 10  # Base priority

                            # Check type effectiveness
                            effectiveness = TYPE_CHART.get_multiplier_dual_type(
                                m.type,
                                player_defender.types[0],
                                player_defender.types[1] if len(player_defender.types) > 1 else player_defender.types[0]
                            )

                            # Adjust priority based on effectiveness
                            if effectiveness > 1.0:  # Super effective
                                priority -= 1  # Favor this move
                            elif effectiveness < 1.0:  # Not very effective
                                priority += 1  # Avoid this move

                            move_priorities.append((m, priority))

                        # Find minimum priority (best moves)
                        min_priority = min(p for _, p in move_priorities)
                        best_moves = [m for m, p in move_priorities if p == min_priority]

                        # DETERMINISTIC selection for graph exploration (prevents state explosion)
                        # Pick highest power move among best moves for consistent state graph
                        best_move = max(best_moves, key=lambda m: m.power)

                        counter_damage = DamageCalculator.calculate_damage(
                            opponent_attacker, player_defender, best_move
                        )
                        player_defender.take_damage(counter_damage)
                        best_move.use()

                        # If player Pokemon fainted, switch to next available
                        if player_defender.is_fainted():
                            next_state._auto_switch_player()

            # Increment turn
            next_state.turn += 1

            # Add to successors (auto-switch handles Pokemon changes)
            successors.append((next_state, move, damage))

        # TODO: Add switch actions if include_switches=True
        # For now, we focus on attack actions only

        return successors

    def _auto_switch_opponent(self):
        """
        Automatically switch opponent to next alive Pokemon.

        Called when active opponent Pokemon faints.
        """
        for i, pokemon in enumerate(self.opponent_team):
            if not pokemon.is_fainted() and i != self.opponent_active:
                self.opponent_active = i
                return

        # If no alive Pokemon found, battle is over
        # (opponent_active stays on fainted Pokemon)

    def _auto_switch_player(self):
        """
        Automatically switch player to next alive Pokemon.

        Called when active player Pokemon faints.
        """
        for i, pokemon in enumerate(self.player_team):
            if not pokemon.is_fainted() and i != self.player_active:
                self.player_active = i
                return

        # If no alive Pokemon found, battle is over
        # (player_active stays on fainted Pokemon)

    def get_total_damage_dealt_to_opponent(self) -> int:
        """
        Calculate total damage dealt to opponent team.

        Returns:
            Sum of (max_hp - current_hp) for all opponent Pokemon
        """
        total = 0
        for pokemon in self.opponent_team:
            damage = pokemon.max_hp - pokemon.current_hp
            total += damage
        return total

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"BattleState(turn={self.turn}, "
                f"player_active={self.player_active}, "
                f"opponent_active={self.opponent_active}, "
                f"player_alive={self.get_alive_pokemon_count(True)}, "
                f"opponent_alive={self.get_alive_pokemon_count(False)})")

    def __str__(self) -> str:
        """User-friendly string representation."""
        player = self.get_active_player_pokemon()
        opponent = self.get_active_opponent_pokemon()

        return (f"Turn {self.turn}\n"
                f"Player: {player}\n"
                f"Opponent: {opponent}")

    def to_dict(self) -> dict:
        """
        Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation
        """
        return {
            "player_team": [p.to_dict() for p in self.player_team],
            "opponent_team": [p.to_dict() for p in self.opponent_team],
            "player_active": self.player_active,
            "opponent_active": self.opponent_active,
            "turn": self.turn,
            "battle_over": self.is_battle_over(),
            "player_won": self.player_won() if self.is_battle_over() else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'BattleState':
        """
        Create a BattleState from a dictionary.

        Args:
            data: Dictionary with battle state data

        Returns:
            New BattleState instance
        """
        player_team = [Pokemon.from_dict(p) for p in data["player_team"]]
        opponent_team = [Pokemon.from_dict(p) for p in data["opponent_team"]]

        return BattleState(
            player_team=player_team,
            opponent_team=opponent_team,
            player_active=data.get("player_active", 0),
            opponent_active=data.get("opponent_active", 0),
            turn=data.get("turn", 0)
        )
