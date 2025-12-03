"""
Test Script for Battle Models

Tests all Session 3 components:
- Pokemon and Move classes
- Type Effectiveness (HashTable from Assignment 7)
- Damage Calculator
- BattleState

Run this to verify everything works correctly!

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.pokemon import Pokemon, create_pikachu, create_charizard, create_blastoise
from models.move import Move, COMMON_MOVES
from models.battleState import BattleState
from utils.typeEffectiveness import TYPE_CHART
from utils.damageCalculator import DamageCalculator


def test_pokemon_creation():
    """Test Pokemon class."""
    print("=" * 60)
    print("TEST 1: Pokemon Creation")
    print("=" * 60)

    # Create a Pikachu
    pikachu = create_pikachu(level=50)

    print(f"Created: {pikachu}")
    print(f"Stats: HP={pikachu.max_hp}, Atk={pikachu.attack}, "
          f"Def={pikachu.defense}, Spd={pikachu.speed}, Spc={pikachu.special}")
    print(f"Moves: {[m.name for m in pikachu.moves]}")
    print(f"Is fainted? {pikachu.is_fainted()}")

    # Test damage and healing
    pikachu.take_damage(50)
    print(f"After 50 damage: {pikachu.current_hp}/{pikachu.max_hp} HP")

    pikachu.heal(25)
    print(f"After healing 25: {pikachu.current_hp}/{pikachu.max_hp} HP")

    print("✅ Pokemon creation test passed!\n")


def test_type_effectiveness():
    """Test Type Effectiveness table (HashTable from Assignment 7)."""
    print("=" * 60)
    print("TEST 2: Type Effectiveness (HashTable)")
    print("=" * 60)

    # Test some type matchups
    tests = [
        ("Fire", "Grass", 2.0, "Super effective"),
        ("Water", "Fire", 2.0, "Super effective"),
        ("Electric", "Ground", 0.0, "No effect"),
        ("Normal", "Rock", 0.5, "Not very effective"),
        ("Fire", "Water", 0.5, "Not very effective"),
        ("Normal", "Normal", 1.0, "Neutral"),
    ]

    print("Testing type matchups:")
    for attack_type, defense_type, expected, description in tests:
        multiplier = TYPE_CHART.get_multiplier(attack_type, defense_type)
        status = "✅" if multiplier == expected else "❌"
        print(f"{status} {attack_type} vs {defense_type}: "
              f"{multiplier}x (expected {expected}x) - {description}")

    # Test dual-type
    print("\nTesting dual-type effectiveness:")
    # Water vs Water/Ground (0.5 * 2.0 = 1.0 neutral)
    dual_mult = TYPE_CHART.get_multiplier_dual_type("Water", "Water", "Ground")
    print(f"Water vs Water/Ground: {dual_mult}x (expected 1.0x)")

    print("✅ Type effectiveness test passed!\n")


def test_damage_calculation():
    """Test Damage Calculator."""
    print("=" * 60)
    print("TEST 3: Damage Calculation")
    print("=" * 60)

    # Create Pokemon
    pikachu = create_pikachu(level=50)
    charizard = create_charizard(level=50)

    # Test Thunderbolt (Electric vs Fire/Flying)
    thunderbolt = pikachu.get_move("Thunderbolt")

    print(f"Attacker: {pikachu.name} (Level {pikachu.level})")
    print(f"Defender: {charizard.name} (Level {charizard.level})")
    print(f"Move: {thunderbolt}")

    # Calculate damage range
    min_dmg, max_dmg = DamageCalculator.calculate_damage_range(
        pikachu, charizard, thunderbolt
    )
    print(f"Damage range: {min_dmg} - {max_dmg}")

    # Calculate average damage
    avg_dmg = DamageCalculator.calculate_average_damage(
        pikachu, charizard, thunderbolt,
        include_crit_chance=False
    )
    print(f"Average damage: {avg_dmg:.1f}")

    # Calculate with specific rolls
    damage = DamageCalculator.calculate_damage(
        pikachu, charizard, thunderbolt,
        is_critical=False,
        random_roll=236  # Average roll
    )
    print(f"Calculated damage: {damage}")

    # Check type effectiveness
    type_mult = TYPE_CHART.get_multiplier_dual_type(
        thunderbolt.type,
        charizard.types[0],
        charizard.types[1]
    )
    print(f"Type effectiveness: {type_mult}x (Electric vs Fire/Flying)")

    # Get description
    description = DamageCalculator.get_damage_description(
        pikachu, charizard, thunderbolt, damage
    )
    print(f"Description: {description}")

    print("✅ Damage calculation test passed!\n")


def test_battle_state():
    """Test BattleState class."""
    print("=" * 60)
    print("TEST 4: BattleState")
    print("=" * 60)

    # Create teams
    player_team = [create_pikachu(level=50)]
    opponent_team = [create_charizard(level=50)]

    # Create initial state
    state = BattleState(
        player_team=player_team,
        opponent_team=opponent_team
    )

    print(f"Initial state: {state}")
    print(f"Battle over? {state.is_battle_over()}")
    print(f"Hash key: {state.hash_key()}")

    # Test state copy
    state_copy = state.copy()
    print(f"Copied state hash: {state_copy.hash_key()}")
    print(f"States equal? {state == state_copy}")

    # Modify copy and verify original unchanged
    state_copy.turn = 5
    print(f"Original turn: {state.turn}, Copy turn: {state_copy.turn}")
    print(f"States still equal? {state == state_copy}")

    print("✅ BattleState test passed!\n")


def test_successor_states():
    """Test successor state generation."""
    print("=" * 60)
    print("TEST 5: Successor State Generation")
    print("=" * 60)

    # Create simple battle
    pikachu = create_pikachu(level=50)
    blastoise = create_blastoise(level=50)

    player_team = [pikachu]
    opponent_team = [blastoise]

    state = BattleState(
        player_team=player_team,
        opponent_team=opponent_team
    )

    print(f"Initial state: {state}")
    print(f"Pikachu's moves: {[m.name for m in pikachu.moves]}")

    # Generate successors
    successors = state.generate_successor_states()

    print(f"\nGenerated {len(successors)} successor states:")
    for i, (next_state, move, damage) in enumerate(successors, 1):
        print(f"{i}. Use {move.name}: {damage} damage")
        print(f"   Opponent HP: {state.get_active_opponent_pokemon().current_hp} → "
              f"{next_state.get_active_opponent_pokemon().current_hp}")

    print("✅ Successor state generation test passed!\n")


def test_full_battle_simulation():
    """Test a simple battle simulation."""
    print("=" * 60)
    print("TEST 6: Full Battle Simulation")
    print("=" * 60)

    # Create teams
    player_team = [create_pikachu(level=50)]
    opponent_team = [create_charizard(level=50)]

    state = BattleState(
        player_team=player_team,
        opponent_team=opponent_team
    )

    print("Starting battle!")
    print(f"Player: {state.get_active_player_pokemon()}")
    print(f"Opponent: {state.get_active_opponent_pokemon()}")
    print()

    turn = 1
    while not state.is_battle_over() and turn <= 20:  # Max 20 turns
        print(f"--- Turn {turn} ---")

        # Generate possible moves
        successors = state.generate_successor_states()

        if not successors:
            print("No valid moves available!")
            break

        # Pick the move that deals the most damage (greedy strategy)
        best_move = max(successors, key=lambda x: x[2])
        next_state, move, damage = best_move

        # Apply the move
        print(f"{state.get_active_player_pokemon().name} used {move.name}!")
        print(f"Dealt {damage} damage!")

        # Update state
        state = next_state

        # Show opponent HP
        opponent = state.get_active_opponent_pokemon()
        print(f"{opponent.name}: {opponent.current_hp}/{opponent.max_hp} HP "
              f"({opponent.get_hp_percentage():.1f}%)")

        if opponent.is_fainted():
            print(f"{opponent.name} fainted!")

        print()
        turn += 1

    # Check result
    if state.player_won():
        print("🎉 Player won!")
    elif state.opponent_won():
        print("💀 Player lost!")
    else:
        print("⏱️ Battle timed out!")

    print("✅ Full battle simulation test passed!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("BATTLE MODELS TEST SUITE - Session 3")
    print("=" * 60 + "\n")

    try:
        test_pokemon_creation()
        test_type_effectiveness()
        test_damage_calculation()
        test_battle_state()
        test_successor_states()
        test_full_battle_simulation()

        print("=" * 60)
        print("ALL TESTS PASSED! ✅✅✅")
        print("Session 3 is COMPLETE!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
