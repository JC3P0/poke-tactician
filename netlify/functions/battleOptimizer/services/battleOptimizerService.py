"""
Battle Optimizer Service - Main Facade for Battle Optimization

This service is the main entry point for battle optimization.
It orchestrates all the pieces:
- Pokemon data conversion
- Boss trainer loading
- Algorithm execution
- Result formatting

Architecture Pattern: Facade
- Provides simple, unified interface for complex operations
- Hides implementation details from callers
- Makes it easy to swap algorithms or data sources

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os
from typing import Dict, List, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pokemonDataService import PokemonDataService
from data.bossTrainers import get_boss_trainer
from algorithms.greedy import run_greedy_optimizer, GreedyResult
from algorithms.dynamic_programming import run_dp_optimizer, DPResult
from algorithms.dijkstra import run_dijkstra_optimizer, DijkstraResult
from models.pokemon import Pokemon


class BattleOptimizerService:
    """
    Main facade for battle optimization.

    This service provides a simple interface for:
    1. Converting MongoDB Pokemon data to battle-ready Pokemon
    2. Running optimization algorithms
    3. Formatting results for API responses
    """

    @staticmethod
    def optimize_battle(
        player_team_data: List[Dict[str, Any]],
        opponent_team_data: Optional[List[Dict[str, Any]]] = None,
        boss_trainer_id: Optional[str] = None,
        algorithm: str = "dijkstra",
        player_level: int = 50,
        max_turns: int = 75,  # Balanced: Allows long battles but prevents runaway
        max_depth: int = 40,  # DP: Reasonable depth with memoization
        max_states: int = 20000  # Dijkstra: Big reduction but enough for complex battles
    ) -> Dict[str, Any]:
        """
        Optimize a Pokemon battle using the specified algorithm.

        This is the main entry point for the battle optimizer!

        Args:
            player_team_data: List of MongoDB Pokemon data for player's team
            opponent_team_data: Optional list of MongoDB Pokemon data for opponent
            boss_trainer_id: Optional boss trainer ID ("blue", "giovanni", "lance")
            algorithm: Which algorithm to use ("greedy", "dp", "dijkstra")
            player_level: Level for player's Pokemon (default 50)
            max_turns: Max turns for greedy algorithm (default 100)
            max_depth: Max depth for DP algorithm (default 50)
            max_states: Max states for Dijkstra algorithm (default 100,000)

        Returns:
            Dictionary with optimization results

        Raises:
            ValueError: If invalid algorithm or missing opponent data
        """

        # Validate algorithm
        if algorithm not in ["greedy", "dp", "dijkstra"]:
            raise ValueError(f"Invalid algorithm: {algorithm}")

        # Convert player team from MongoDB format
        player_team = PokemonDataService.from_mongodb_list(
            player_team_data,
            level=player_level
        )

        # Get opponent team (either custom or boss trainer)
        if boss_trainer_id:
            boss_data = get_boss_trainer(boss_trainer_id)
            opponent_team = boss_data['team']
            opponent_name = boss_data['name']
        elif opponent_team_data:
            opponent_team = PokemonDataService.from_mongodb_list(
                opponent_team_data,
                level=player_level
            )
            opponent_name = "Custom Opponent"
        else:
            raise ValueError("Must provide either opponent_team_data or boss_trainer_id")

        # Create initial battle state for replay
        from models.battleState import BattleState
        initial_state = BattleState(player_team, opponent_team)

        # Run the selected algorithm
        if algorithm == "greedy":
            result = run_greedy_optimizer(player_team, opponent_team, max_turns=max_turns)
            formatted_result = BattleOptimizerService._format_greedy_result(result, initial_state)
        elif algorithm == "dp":
            result = run_dp_optimizer(player_team, opponent_team, max_depth=max_depth)
            formatted_result = BattleOptimizerService._format_dp_result(result, initial_state)
        else:  # dijkstra
            result = run_dijkstra_optimizer(player_team, opponent_team, max_states=max_states)
            formatted_result = BattleOptimizerService._format_dijkstra_result(result, initial_state)

        # Add metadata
        formatted_result["algorithm"] = algorithm
        formatted_result["opponent"] = opponent_name
        formatted_result["playerTeamSize"] = len(player_team)
        formatted_result["opponentTeamSize"] = len(opponent_team)

        # Add opponent team details for display
        formatted_result["opponentTeam"] = [
            {
                "name": p.name,
                "level": p.level,
                "types": p.types,
                "maxHp": p.max_hp
            }
            for p in opponent_team
        ]

        return formatted_result

    @staticmethod
    def _format_greedy_result(result: GreedyResult, initial_state=None) -> Dict[str, Any]:
        """Format Greedy algorithm result for API response."""
        formatted = {
            "success": result.success,
            "totalDamage": result.total_damage,
            "turns": result.turns,
            "moveSequence": result.move_sequence,
            "victory": result.success
        }

        # Add detailed battle log
        if initial_state and result.move_sequence:
            from utils.battleReplay import replay_battle
            formatted["battleLog"] = replay_battle(initial_state, result.move_sequence)

        return formatted

    @staticmethod
    def _format_dp_result(result: DPResult, initial_state=None) -> Dict[str, Any]:
        """Format DP algorithm result for API response."""
        formatted = {
            "success": result.success,
            "totalDamage": result.total_damage,
            "turns": result.turns,
            "moveSequence": result.move_sequence,
            "victory": result.success,
            "cacheHits": result.cache_hits,
            "cacheMisses": result.cache_misses,
            "cacheHitRate": result.get_cache_hit_rate(),
            "statesExplored": result.states_explored
        }

        # Add detailed battle log
        if initial_state and result.move_sequence:
            from utils.battleReplay import replay_battle
            formatted["battleLog"] = replay_battle(initial_state, result.move_sequence)

        return formatted

    @staticmethod
    def _format_dijkstra_result(result: DijkstraResult, initial_state=None) -> Dict[str, Any]:
        """Format Dijkstra algorithm result for API response."""
        formatted = {
            "success": result.success,
            "totalDamage": result.total_damage,
            "turns": result.turns,
            "moveSequence": result.move_sequence,
            "victory": result.success,
            "statesExplored": result.states_explored,
            "pathCost": result.path_cost
        }

        # Add detailed battle log
        if initial_state and result.move_sequence:
            from utils.battleReplay import replay_battle
            formatted["battleLog"] = replay_battle(initial_state, result.move_sequence)

        return formatted

    @staticmethod
    def get_boss_trainers() -> Dict[str, Any]:
        """
        Get list of available boss trainers.

        Returns:
            Dictionary mapping boss IDs to trainer info
        """
        from data.bossTrainers import BOSS_TRAINERS

        # Return metadata only (not the actual teams)
        return {
            boss_id: {
                "name": data["name"],
                "title": data["title"],
                "description": data["description"]
            }
            for boss_id, data in BOSS_TRAINERS.items()
        }
