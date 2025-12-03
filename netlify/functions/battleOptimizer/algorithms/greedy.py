"""
Greedy Battle Algorithm - Uses Heap (CS_311 Assignment 6)

Implements a greedy strategy for Pokemon battles:
- At each turn, calculate damage for all available moves
- Use a max-heap to select the highest damage move
- Apply that move and repeat

This is the BASELINE algorithm to compare against DP and Dijkstra.

Performance Characteristics:
- Time: O(T * M * log M) where T = turns, M = moves per Pokemon
- Space: O(M) for the heap
- Optimality: NOT OPTIMAL - greedy choices may not lead to global optimum

Uses: Heap from CS_311 Assignment 6

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os
from typing import List, Tuple, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataStructures.heap import Heap
from models.battleState import BattleState
from models.pokemon import Pokemon
from models.move import Move
from utils.damageCalculator import DamageCalculator


class GreedyResult:
    """
    Result from the greedy algorithm.

    Attributes:
        success: Whether the player won
        total_damage: Total damage dealt to opponent
        turns: Number of turns taken
        move_sequence: List of moves used (in order)
        final_state: Final battle state
    """

    def __init__(
        self,
        success: bool,
        total_damage: int,
        turns: int,
        move_sequence: List[str],
        final_state: BattleState
    ):
        self.success = success
        self.total_damage = total_damage
        self.turns = turns
        self.move_sequence = move_sequence
        self.final_state = final_state

    def __repr__(self) -> str:
        return (f"GreedyResult(success={self.success}, "
                f"total_damage={self.total_damage}, "
                f"turns={self.turns}, "
                f"moves={len(self.move_sequence)})")


class GreedyBattleOptimizer:
    """
    Greedy battle optimizer using Heap (CS_311 Assignment 6).

    Strategy: Always pick the move that deals the most damage RIGHT NOW.
    Does not consider future states or long-term strategy.
    """

    def __init__(self, max_turns: int = 100):
        """
        Create a greedy optimizer.

        Args:
            max_turns: Maximum turns before giving up (prevents infinite loops)
        """
        self.max_turns = max_turns

    def optimize(self, initial_state: BattleState) -> GreedyResult:
        """
        Run the greedy algorithm on a battle.

        Algorithm:
        1. While battle not over and turns < max:
           a. Get all available moves for active Pokemon
           b. Calculate damage for each move
           c. Insert (damage, move) into max-heap
           d. Extract max from heap
           e. Apply that move to get next state
           f. Repeat

        Args:
            initial_state: Starting battle state

        Returns:
            GreedyResult with outcome and statistics

        Time Complexity: O(T * M * log M)
            - T = number of turns (worst case: max_turns)
            - M = number of moves (usually 4)
            - log M = heap operations

        Space Complexity: O(M) for the heap
        """
        current_state = initial_state.copy()
        move_sequence = []
        turns = 0

        while not current_state.is_battle_over() and turns < self.max_turns:
            # Get the best move using max-heap
            best_move_name = self._select_best_move(current_state)

            if best_move_name is None:
                # No valid moves available (shouldn't happen)
                break

            # Record the move
            move_sequence.append(best_move_name)

            # Apply the move (generate successor state)
            successors = current_state.generate_successor_states()

            # Find the successor that used our selected move
            next_state = None
            for state, move, damage in successors:
                if move.name == best_move_name:
                    next_state = state
                    break

            if next_state is None:
                # Move not found (shouldn't happen)
                break

            # Move to next state
            current_state = next_state
            turns += 1

        # Calculate final statistics
        success = current_state.player_won()
        total_damage = current_state.get_total_damage_dealt_to_opponent()

        return GreedyResult(
            success=success,
            total_damage=total_damage,
            turns=turns,
            move_sequence=move_sequence,
            final_state=current_state
        )

    def _select_best_move(self, state: BattleState) -> Optional[str]:
        """
        Select the move that deals the most damage using a max-heap.

        This is where we use the Heap from Assignment 6!

        Args:
            state: Current battle state

        Returns:
            Name of the move that deals most damage, or None if no moves

        Time Complexity: O(M log M) where M = number of moves
        """
        active_player = state.get_active_player_pokemon()
        active_opponent = state.get_active_opponent_pokemon()

        # Create a max-heap for move selection
        # Heap from CS_311 Assignment 6!
        move_heap = Heap()

        # Calculate damage for each move
        for move in active_player.moves:
            if not move.is_usable():
                continue  # Skip moves with 0 PP

            # Calculate damage
            damage = DamageCalculator.calculate_average_damage(
                active_player,
                active_opponent,
                move,
                include_crit_chance=False
            )

            # Insert (damage, move_name) into max-heap
            # Heap.insert takes a value, we'll use tuples: (damage, move_name)
            move_heap.insert((damage, move.name))

        # Extract the maximum (highest damage move)
        if move_heap.is_empty():
            return None

        max_item = move_heap.remove_max()
        damage, move_name = max_item

        return move_name


def run_greedy_optimizer(
    player_team: List[Pokemon],
    opponent_team: List[Pokemon],
    max_turns: int = 100
) -> GreedyResult:
    """
    Convenience function to run greedy optimizer on teams.

    Args:
        player_team: Player's Pokemon team
        opponent_team: Opponent's Pokemon team
        max_turns: Maximum turns before timeout

    Returns:
        GreedyResult with outcome
    """
    initial_state = BattleState(
        player_team=player_team,
        opponent_team=opponent_team
    )

    optimizer = GreedyBattleOptimizer(max_turns=max_turns)
    return optimizer.optimize(initial_state)
