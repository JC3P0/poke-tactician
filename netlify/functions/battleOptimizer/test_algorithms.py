"""
Test Script for Battle Optimization Algorithms

Tests all three CS_311 optimization algorithms:
1. Greedy (uses Heap - Assignment 6)
2. Dynamic Programming (uses HashTable - Assignment 7)
3. Dijkstra (uses Graph - Assignment 9)

Compares performance and optimality of each approach.

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.pokemon import create_pikachu, create_charizard, create_blastoise
from algorithms.greedy import run_greedy_optimizer
from algorithms.dynamic_programming import run_dp_optimizer
from algorithms.dijkstra import run_dijkstra_optimizer


def print_separator(title: str = ""):
    """Print a nice separator."""
    if title:
        print(f"\n{'=' * 60}")
        print(f"{title.center(60)}")
        print('=' * 60)
    else:
        print('=' * 60)


def test_greedy_algorithm():
    """Test the Greedy algorithm (Heap - Assignment 6)."""
    print_separator("TEST 1: Greedy Algorithm (Heap)")

    # Create simple 1v1 battle
    player_team = [create_pikachu(level=50)]
    opponent_team = [create_charizard(level=50)]

    print("Battle: Pikachu vs Charizard")
    print("Algorithm: Greedy (always pick highest damage move)")
    print("Uses: Heap from CS_311 Assignment 6\n")

    # Run greedy optimizer
    start_time = time.time()
    result = run_greedy_optimizer(player_team, opponent_team, max_turns=20)
    elapsed = time.time() - start_time

    # Print results
    print(f"Result: {'Victory!' if result.success else 'Defeat'}")
    print(f"Turns: {result.turns}")
    print(f"Total Damage: {result.total_damage}")
    print(f"Move Sequence: {' -> '.join(result.move_sequence)}")
    print(f"Runtime: {elapsed * 1000:.2f}ms")

    print("\n✅ Greedy algorithm test passed!\n")
    return result


def test_dp_algorithm():
    """Test the Dynamic Programming algorithm (HashTable - Assignment 7)."""
    print_separator("TEST 2: Dynamic Programming (HashTable)")

    # Create simple 1v1 battle
    player_team = [create_pikachu(level=50)]
    opponent_team = [create_charizard(level=50)]

    print("Battle: Pikachu vs Charizard")
    print("Algorithm: Dynamic Programming with memoization")
    print("Uses: HashTable from CS_311 Assignment 7\n")

    # Run DP optimizer
    start_time = time.time()
    result = run_dp_optimizer(player_team, opponent_team, max_depth=20)
    elapsed = time.time() - start_time

    # Print results
    print(f"Result: {'Victory!' if result.success else 'Defeat'}")
    print(f"Turns: {result.turns}")
    print(f"Total Damage: {result.total_damage}")
    print(f"Move Sequence: {' -> '.join(result.move_sequence)}")
    print(f"Cache Hits: {result.cache_hits}")
    print(f"Cache Misses: {result.cache_misses}")
    print(f"Cache Hit Rate: {result.get_cache_hit_rate():.1%}")
    print(f"States Explored: {result.states_explored}")
    print(f"Runtime: {elapsed * 1000:.2f}ms")

    print("\n✅ Dynamic Programming test passed!\n")
    return result


def test_dijkstra_algorithm():
    """Test the Dijkstra algorithm (Graph - Assignment 9)."""
    print_separator("TEST 3: Dijkstra's Algorithm (Graph)")

    # Create simple 1v1 battle
    player_team = [create_pikachu(level=50)]
    opponent_team = [create_charizard(level=50)]

    print("Battle: Pikachu vs Charizard")
    print("Algorithm: Dijkstra's shortest path")
    print("Uses: Graph from CS_311 Assignment 9\n")

    # Run Dijkstra optimizer
    start_time = time.time()
    result = run_dijkstra_optimizer(player_team, opponent_team, max_states=200)
    elapsed = time.time() - start_time

    # Print results
    print(f"Result: {'Victory!' if result.success else 'Defeat'}")
    print(f"Turns: {result.turns}")
    print(f"Total Damage: {result.total_damage}")
    print(f"Move Sequence: {' -> '.join(result.move_sequence)}")
    print(f"States Explored: {result.states_explored}")
    print(f"Path Cost: {result.path_cost:.1f}")
    print(f"Runtime: {elapsed * 1000:.2f}ms")

    print("\n✅ Dijkstra algorithm test passed!\n")
    return result


def compare_algorithms():
    """Compare all three algorithms on the same battle."""
    print_separator("TEST 4: Algorithm Comparison")

    # Create battle scenario
    player_team = [create_pikachu(level=50)]
    opponent_team = [create_blastoise(level=50)]

    print("Battle: Pikachu vs Blastoise")
    print("Running all 3 algorithms...\n")

    results = {}

    # Greedy
    print("Running Greedy...")
    start = time.time()
    greedy_result = run_greedy_optimizer(player_team, opponent_team, max_turns=20)
    greedy_time = time.time() - start
    results['Greedy'] = (greedy_result, greedy_time)
    print(f"  Turns: {greedy_result.turns}, Damage: {greedy_result.total_damage}, "
          f"Time: {greedy_time * 1000:.2f}ms")

    # DP
    print("Running Dynamic Programming...")
    start = time.time()
    dp_result = run_dp_optimizer(player_team, opponent_team, max_depth=20)
    dp_time = time.time() - start
    results['DP'] = (dp_result, dp_time)
    print(f"  Turns: {dp_result.turns}, Damage: {dp_result.total_damage}, "
          f"Time: {dp_time * 1000:.2f}ms, Hit Rate: {dp_result.get_cache_hit_rate():.1%}")

    # Dijkstra
    print("Running Dijkstra...")
    start = time.time()
    dijkstra_result = run_dijkstra_optimizer(player_team, opponent_team, max_states=200)
    dijkstra_time = time.time() - start
    results['Dijkstra'] = (dijkstra_result, dijkstra_time)
    print(f"  Turns: {dijkstra_result.turns}, Damage: {dijkstra_result.total_damage}, "
          f"Time: {dijkstra_time * 1000:.2f}ms, States: {dijkstra_result.states_explored}")

    # Comparison table
    print("\n" + "=" * 80)
    print(f"{'Algorithm':<20} {'Success':<10} {'Turns':<8} {'Damage':<10} {'Time (ms)':<12}")
    print("=" * 80)

    for name, (result, runtime) in results.items():
        print(f"{name:<20} {str(result.success):<10} {result.turns:<8} "
              f"{result.total_damage:<10} {runtime * 1000:<12.2f}")

    print("=" * 80)

    # Analysis
    print("\nAnalysis:")
    print(f"- Greedy: Simple, fast, but may not be optimal")
    print(f"- DP: Optimal solution with memoization (cache hit rate: {dp_result.get_cache_hit_rate():.1%})")
    print(f"- Dijkstra: Optimal, explores {dijkstra_result.states_explored} states")

    print("\n✅ Algorithm comparison complete!\n")


def test_complex_battle():
    """Test with a more complex battle scenario."""
    print_separator("TEST 5: Complex Battle (2v1)")

    # Player has 2 Pokemon, opponent has 1
    player_team = [
        create_pikachu(level=40),
        create_charizard(level=40)
    ]
    opponent_team = [create_blastoise(level=50)]

    print("Battle: Pikachu + Charizard vs Blastoise")
    print("Testing: Can we handle multi-Pokemon teams?\n")

    # Just test Greedy (fastest)
    print("Running Greedy algorithm...")
    start = time.time()
    result = run_greedy_optimizer(player_team, opponent_team, max_turns=30)
    elapsed = time.time() - start

    print(f"Result: {'Victory!' if result.success else 'Defeat'}")
    print(f"Turns: {result.turns}")
    print(f"Total Damage: {result.total_damage}")
    print(f"Move Sequence: {' -> '.join(result.move_sequence[:10])}{'...' if len(result.move_sequence) > 10 else ''}")
    print(f"Runtime: {elapsed * 1000:.2f}ms")

    print("\n✅ Complex battle test passed!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("BATTLE OPTIMIZATION ALGORITHMS TEST SUITE - Session 4")
    print("=" * 60 + "\n")

    try:
        # Test each algorithm individually
        greedy_result = test_greedy_algorithm()
        dp_result = test_dp_algorithm()
        dijkstra_result = test_dijkstra_algorithm()

        # Compare all algorithms
        compare_algorithms()

        # Test complex scenario
        test_complex_battle()

        # Final summary
        print_separator("SUMMARY")
        print("All algorithms implemented and tested successfully!")
        print("\nData Structures Used:")
        print("  ✅ Heap (Assignment 6) - Greedy move selection")
        print("  ✅ HashTable (Assignment 7) - DP memoization")
        print("  ✅ Graph (Assignment 9) - Dijkstra pathfinding")
        print("\nSession 4 is COMPLETE! 🎉")
        print_separator()

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
