"""
Battle Replay System - Detailed Battle Log Generator

Takes a move sequence and replays the battle with full HP/damage tracking.

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

from typing import List, Dict, Any
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.battleState import BattleState
from models.pokemon import Pokemon
from utils.damageCalculator import DamageCalculator
from utils.typeEffectiveness import TYPE_CHART


class BattleEvent:
    """Represents a single event in the battle."""

    def __init__(self, event_type: str, **kwargs):
        self.type = event_type  # "attack", "faint", "switch"
        self.data = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            **self.data
        }


def replay_battle(
    initial_state: BattleState,
    move_sequence: List[str]
) -> tuple[List[Dict[str, Any]], BattleState]:
    """
    Replay a battle with detailed logging.

    Args:
        initial_state: Starting battle state
        move_sequence: List of move names (auto-switch handles Pokemon changes)

    Returns:
        Tuple of (battle_log, final_state)
        - battle_log: List of battle events with full details
        - final_state: Final battle state after all moves executed
    """
    battle_log = []
    state = initial_state.copy()

    for turn_num, move_name in enumerate(move_sequence, 1):
        # Get active Pokemon (auto-switch handles Pokemon changes)
        player_pokemon = state.get_active_player_pokemon()
        opponent_pokemon = state.get_active_opponent_pokemon()

        # Check if player has lost (all Pokemon fainted)
        if player_pokemon.is_fainted():
            # Battle is over
            break

        # Get the move for current active Pokemon
        player_move = player_pokemon.get_move(move_name)
        if not player_move:
            continue

        # Player attacks
        player_hp_before = player_pokemon.current_hp
        opponent_hp_before = opponent_pokemon.current_hp

        damage = DamageCalculator.calculate_damage(
            player_pokemon, opponent_pokemon, player_move,
            is_critical=False,  # No critical hits for consistency
            random_roll=236  # Average of 217-255 for deterministic damage
        )
        opponent_pokemon.take_damage(damage)

        effectiveness = TYPE_CHART.get_multiplier_dual_type(
            player_move.type,
            opponent_pokemon.types[0],
            opponent_pokemon.types[1] if len(opponent_pokemon.types) > 1 else opponent_pokemon.types[0]
        )

        battle_log.append({
            "turn": turn_num,
            "event": "player_attack",
            "attacker": {
                "name": player_pokemon.name,
                "hp": player_hp_before,
                "maxHp": player_pokemon.max_hp
            },
            "defender": {
                "name": opponent_pokemon.name,
                "hpBefore": opponent_hp_before,
                "hpAfter": opponent_pokemon.current_hp,
                "maxHp": opponent_pokemon.max_hp
            },
            "move": player_move.name,
            "damage": damage,
            "effectiveness": effectiveness
        })

        # Check if opponent fainted
        if opponent_pokemon.is_fainted():
            battle_log.append({
                "turn": turn_num,
                "event": "faint",
                "pokemon": {
                    "name": opponent_pokemon.name,
                    "team": "opponent"
                }
            })

            # Try to switch opponent
            state._auto_switch_opponent()
            new_opponent = state.get_active_opponent_pokemon()

            if new_opponent.current_hp > 0:
                battle_log.append({
                    "turn": turn_num,
                    "event": "switch",
                    "pokemon": {
                        "name": new_opponent.name,
                        "hp": new_opponent.current_hp,
                        "maxHp": new_opponent.max_hp,
                        "team": "opponent"
                    }
                })
        else:
            # Opponent counterattacks (Gen 1 AI)
            if not state.is_battle_over():
                opponent_pokemon = state.get_active_opponent_pokemon()
                player_pokemon = state.get_active_player_pokemon()

                # Use Gen 1 AI to select move
                usable_moves = [m for m in opponent_pokemon.moves if m.is_usable()]
                if usable_moves:
                    # Calculate priority for each move
                    move_priorities = []
                    for m in usable_moves:
                        priority = 10
                        effectiveness = TYPE_CHART.get_multiplier_dual_type(
                            m.type,
                            player_pokemon.types[0],
                            player_pokemon.types[1] if len(player_pokemon.types) > 1 else player_pokemon.types[0]
                        )

                        if effectiveness > 1.0:
                            priority -= 1
                        elif effectiveness < 1.0:
                            priority += 1

                        move_priorities.append((m, priority))

                    min_priority = min(p for _, p in move_priorities)
                    best_moves = [m for m, p in move_priorities if p == min_priority]
                    # DETERMINISTIC selection (same as battleState.py for consistency)
                    opponent_move = max(best_moves, key=lambda m: m.power)

                    # Opponent attacks
                    opponent_hp_before = opponent_pokemon.current_hp
                    player_hp_before = player_pokemon.current_hp

                    counter_damage = DamageCalculator.calculate_damage(
                        opponent_pokemon, player_pokemon, opponent_move
                    )
                    player_pokemon.take_damage(counter_damage)

                    counter_effectiveness = TYPE_CHART.get_multiplier_dual_type(
                        opponent_move.type,
                        player_pokemon.types[0],
                        player_pokemon.types[1] if len(player_pokemon.types) > 1 else player_pokemon.types[0]
                    )

                    battle_log.append({
                        "turn": turn_num,
                        "event": "opponent_attack",
                        "attacker": {
                            "name": opponent_pokemon.name,
                            "hp": opponent_hp_before,
                            "maxHp": opponent_pokemon.max_hp
                        },
                        "defender": {
                            "name": player_pokemon.name,
                            "hpBefore": player_hp_before,
                            "hpAfter": player_pokemon.current_hp,
                            "maxHp": player_pokemon.max_hp
                        },
                        "move": opponent_move.name,
                        "damage": counter_damage,
                        "effectiveness": counter_effectiveness
                    })

                    # Check if player fainted
                    if player_pokemon.is_fainted():
                        battle_log.append({
                            "turn": turn_num,
                            "event": "faint",
                            "pokemon": {
                                "name": player_pokemon.name,
                                "team": "player"
                            }
                        })

                        # Try to switch player
                        state._auto_switch_player()
                        new_player = state.get_active_player_pokemon()

                        if new_player.current_hp > 0:
                            battle_log.append({
                                "turn": turn_num,
                                "event": "switch",
                                "pokemon": {
                                    "name": new_player.name,
                                    "hp": new_player.current_hp,
                                    "maxHp": new_player.max_hp,
                                    "team": "player"
                                }
                            })

        # Check if battle is over
        if state.is_battle_over():
            battle_log.append({
                "turn": turn_num,
                "event": "battle_end",
                "winner": "player" if state.player_won() else "opponent"
            })
            break

    return battle_log, state
