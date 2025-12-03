"""
Dynamic Programming Battle Optimizer - Uses HashTable (CS_311 Assignment 7)

Implements optimal battle strategy using Dynamic Programming with memoization:
- Define recursive relation: optimalDamage(state) = max(damage + optimalDamage(nextState))
- Use HashTable to cache computed results (memoization)
- Guarantees OPTIMAL solution (unlike greedy)

Performance Characteristics:
- Time: O(S * M) where S = unique states, M = moves per state
- Space: O(S) for the memoization cache
- Optimality: OPTIMAL - finds the best possible strategy

Uses: HashTable from CS_311 Assignment 7 for memoization

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os
from typing import List, Tuple, Optional, Dict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataStructures.hash_table import HashTable
from models.battleState import BattleState
from models.pokemon import Pokemon
from models.move import Move
from utils.damageCalculator import DamageCalculator


class DPResult:
    """
    Result from the DP algorithm.

    Attributes:
        success: Whether the player won
        total_damage: Total damage dealt to opponent
        turns: Number of turns taken
        move_sequence: List of moves used (in order)
        final_state: Final battle state
        cache_hits: Number of cache hits (for analysis)
        cache_misses: Number of cache misses
        states_explored: Total unique states explored
    """

    def __init__(
        self,
        success: bool,
        total_damage: int,
        turns: int,
        move_sequence: List[str],
        final_state: BattleState,
        cache_hits: int = 0,
        cache_misses: int = 0,
        states_explored: int = 0
    ):
        self.success = success
        self.total_damage = total_damage
        self.turns = turns
        self.move_sequence = move_sequence
        self.final_state = final_state
        self.cache_hits = cache_hits
        self.cache_misses = cache_misses
        self.states_explored = states_explored

    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate (0-1)."""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    def __repr__(self) -> str:
        return (f"DPResult(success={self.success}, "
                f"total_damage={self.total_damage}, "
                f"turns={self.turns}, "
                f"cache_hit_rate={self.get_cache_hit_rate():.2%})")


class DynamicProgrammingOptimizer:
    """
    Dynamic Programming optimizer using HashTable memoization (CS_311 Assignment 7).

    Strategy: Use recursion with memoization to find the OPTIMAL move sequence.
    Caches results in HashTable to avoid recomputing the same states.
    """

    def __init__(self, max_depth: int = 50):
        """
        Create a DP optimizer.

        Args:
            max_depth: Maximum recursion depth (prevents stack overflow)
        """
        self.max_depth = max_depth

        # HashTable from Assignment 7 for memoization!
        # Maps: state_hash -> (optimal_damage, best_move_name)
        self.memo = HashTable(size=1000)

        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.states_explored = 0

    def optimize(self, initial_state: BattleState) -> DPResult:
        """
        Run the DP algorithm on a battle.

        Algorithm:
        1. Define recurrence: optimalDamage(state) = max over moves of:
           damage(move) + optimalDamage(nextState)
        2. Base case: if battle over, return 0
        3. Use HashTable to cache results
        4. Reconstruct optimal move sequence

        Args:
            initial_state: Starting battle state

        Returns:
            DPResult with optimal strategy and statistics

        Time Complexity: O(S * M)
            - S = number of unique states explored
            - M = number of moves per state

        Space Complexity: O(S) for the memoization table
        """
        # Reset statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.states_explored = 0

        # Find optimal damage and best move sequence
        move_sequence = []
        current_state = initial_state.copy()
        turns = 0

        while not current_state.is_battle_over() and turns < self.max_depth:
            # Get best move for current state
            best_move = self._get_best_move(current_state, depth=0)

            if best_move is None:
                break

            move_sequence.append(best_move)

            # Apply the move
            successors = current_state.generate_successor_states()
            next_state = None
            for state, move, damage in successors:
                if move.name == best_move:
                    next_state = state
                    break

            if next_state is None:
                break

            current_state = next_state
            turns += 1

        # Calculate final statistics
        success = current_state.player_won()
        total_damage = current_state.get_total_damage_dealt_to_opponent()

        return DPResult(
            success=success,
            total_damage=total_damage,
            turns=turns,
            move_sequence=move_sequence,
            final_state=current_state,
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            states_explored=self.states_explored
        )

    def _get_best_move(self, state: BattleState, depth: int) -> Optional[str]:
        """
        Get the best move for a state using DP.

        Args:
            state: Current battle state
            depth: Current recursion depth

        Returns:
            Name of the best move
        """
        # Get optimal damage and best move from DP
        optimal_damage, best_move = self._compute_optimal(state, depth)
        return best_move

    def _compute_optimal(
        self,
        state: BattleState,
        depth: int
    ) -> Tuple[float, Optional[str]]:
        """
        Compute optimal damage from a state using DP with memoization.

        This is the core DP algorithm!

        Recurrence relation:
            optimalDamage(state) = max over all moves m of:
                damage(m) + optimalDamage(applyMove(state, m))

        Base cases:
            - If battle is over: return 0
            - If max depth reached: return heuristic estimate

        Args:
            state: Current battle state
            depth: Current recursion depth

        Returns:
            Tuple of (optimal_damage, best_move_name)

        Time Complexity: O(M) per unique state (with memoization)
        """
        # Base case: max depth reached
        if depth >= self.max_depth:
            return (0.0, None)

        # Base case: battle is over
        if state.is_battle_over():
            if state.player_won():
                # We won! Return total damage dealt
                return (float(state.get_total_damage_dealt_to_opponent()), None)
            else:
                # We lost or tied
                return (0.0, None)

        # Check if we've already computed this state (MEMOIZATION!)
        state_hash = state.hash_key()
        cached_result = self.memo.get(state_hash)

        if cached_result is not None:
            # Cache hit! (Assignment 7 HashTable lookup = O(1))
            self.cache_hits += 1
            return cached_result

        # Cache miss - need to compute
        self.cache_misses += 1
        self.states_explored += 1

        # Generate all possible successor states
        successors = state.generate_successor_states()

        if not successors:
            # No valid moves
            self.memo.insert(state_hash, (0.0, None))
            return (0.0, None)

        # Find the move that maximizes: immediate_damage + future_optimal_damage
        best_total_damage = -1.0
        best_move_name = None

        for next_state, move, immediate_damage in successors:
            # Recursive call to get optimal damage from next state
            future_damage, _ = self._compute_optimal(next_state, depth + 1)

            # Total damage = immediate + future
            total_damage = immediate_damage + future_damage

            if total_damage > best_total_damage:
                best_total_damage = total_damage
                best_move_name = move.name

        # Cache the result in HashTable (Assignment 7!)
        result = (best_total_damage, best_move_name)
        self.memo.insert(state_hash, result)

        return result


def run_dp_optimizer(
    player_team: List[Pokemon],
    opponent_team: List[Pokemon],
    max_depth: int = 50
) -> DPResult:
    """
    Convenience function to run DP optimizer on teams.

    Args:
        player_team: Player's Pokemon team
        opponent_team: Opponent's Pokemon team
        max_depth: Maximum recursion depth

    Returns:
        DPResult with optimal strategy
    """
    initial_state = BattleState(
        player_team=player_team,
        opponent_team=opponent_team
    )

    optimizer = DynamicProgrammingOptimizer(max_depth=max_depth)
    return optimizer.optimize(initial_state)
