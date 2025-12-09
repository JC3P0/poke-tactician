"""
Dijkstra Battle Optimizer - Uses Graph (CS_311 Assignment 9)

Implements battle optimization using Dijkstra's shortest path algorithm:
- Build a graph where nodes = battle states
- Edges = moves (weighted by inverse damage or turn count)
- Find shortest path from initial state to victory state
- Path represents optimal move sequence

Performance Characteristics:
- Time: O((V + E) log V) where V = states, E = edges (moves)
- Space: O(V + E) for the graph
- Optimality: OPTIMAL for non-negative edge weights

Uses: Graph with Dijkstra from CS_311 Assignment 9

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os
import logging
from typing import List, Tuple, Optional, Dict

# Configure logging for AWS Lambda
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataStructures.graph import Graph, Vertex, Edge
from models.battleState import BattleState
from models.pokemon import Pokemon
from models.move import Move


class DijkstraResult:
    """
    Result from the Dijkstra algorithm.

    Attributes:
        success: Whether the player won
        total_damage: Total damage dealt to opponent
        turns: Number of turns taken
        move_sequence: List of moves used (in order)
        final_state: Final battle state
        states_explored: Total states in the graph
        path_cost: Total cost of the shortest path
    """

    def __init__(
        self,
        success: bool,
        total_damage: int,
        turns: int,
        move_sequence: List[str],
        final_state: BattleState,
        states_explored: int = 0,
        path_cost: float = 0.0
    ):
        self.success = success
        self.total_damage = total_damage
        self.turns = turns
        self.move_sequence = move_sequence
        self.final_state = final_state
        self.states_explored = states_explored
        self.path_cost = path_cost

    def __repr__(self) -> str:
        return (f"DijkstraResult(success={self.success}, "
                f"total_damage={self.total_damage}, "
                f"turns={self.turns}, "
                f"states_explored={self.states_explored})")


class DijkstraBattleOptimizer:
    """
    Battle optimizer using Dijkstra's algorithm (CS_311 Assignment 9).

    Strategy: Build battle state graph and find shortest path to victory.
    """

    def __init__(self, max_states: int = 100000):
        """
        Create a Dijkstra optimizer.

        Args:
            max_states: Maximum states to explore (prevents memory issues)
                       Default: 100,000 (sufficient for most battles)
        """
        self.max_states = max_states

    def optimize(self, initial_state: BattleState) -> DijkstraResult:
        """
        Run Dijkstra's algorithm on a battle.

        Algorithm:
        1. Build battle state graph using BFS
           - Each node = a BattleState
           - Each edge = a move (weight = turn count or inverse damage)
        2. Run Dijkstra from initial state
        3. Find path to any victory state
        4. Extract move sequence from path

        Args:
            initial_state: Starting battle state

        Returns:
            DijkstraResult with optimal strategy

        Time Complexity: O((V + E) log V)
            - V = number of states (vertices)
            - E = number of moves (edges)

        Space Complexity: O(V + E) for the graph
        """
        logger.info(f"[DIJKSTRA] Starting optimization with max_states={self.max_states}")

        # Build the battle state graph
        graph, state_to_vertex, vertex_to_state, move_labels = self._build_graph(
            initial_state
        )

        logger.info(f"[DIJKSTRA] Graph built with {graph.get_num_verts()} vertices")

        if graph.get_num_verts() == 0:
            # No graph built (shouldn't happen)
            return DijkstraResult(
                success=False,
                total_damage=0,
                turns=0,
                move_sequence=[],
                final_state=initial_state,
                states_explored=0
            )

        # Find initial vertex (should be vertex 0)
        initial_vertex_id = 0

        # Find all terminal states (battle over - victory OR defeat)
        terminal_vertices = []
        victory_count = 0
        defeat_count = 0

        for vertex_id in range(graph.get_num_verts()):
            state = vertex_to_state.get(vertex_id)
            if state and state.is_battle_over():
                terminal_vertices.append(vertex_id)
                if state.player_won():
                    victory_count += 1
                else:
                    defeat_count += 1

        logger.info(f"[DIJKSTRA] Found {len(terminal_vertices)} terminal states: {victory_count} victories, {defeat_count} defeats")

        if not terminal_vertices:
            # No terminal state found (shouldn't happen if we explored properly)
            logger.error(f"[DIJKSTRA] No terminal states found after exploring {graph.get_num_verts()} states!")
            return DijkstraResult(
                success=False,
                total_damage=0,
                turns=0,
                move_sequence=[],
                final_state=initial_state,
                states_explored=graph.get_num_verts()
            )

        # Run Dijkstra's algorithm to find the best terminal state
        # Strategy:
        # 1. First, look for victory states (shortest path wins)
        # 2. If no victory possible, find defeat state with maximum damage

        # First pass: Look for victory states
        victory_path = None
        victory_distance = float('inf')
        victory_vertex = None

        # Second pass: Look for best defeat state (max damage)
        defeat_path = None
        defeat_damage = 0
        defeat_vertex = None

        paths_found = 0
        paths_not_found = 0

        for terminal_vertex in terminal_vertices:
            distance, path = graph.dijkstra(initial_vertex_id, terminal_vertex)
            if distance is not None and path:
                paths_found += 1
                state = vertex_to_state.get(terminal_vertex)
                if not state:
                    continue

                damage = state.get_total_damage_dealt_to_opponent()

                if state.player_won():
                    # Victory state - prefer shortest path
                    if distance < victory_distance:
                        victory_distance = distance
                        victory_path = path
                        victory_vertex = terminal_vertex
                else:
                    # Defeat state - prefer maximum damage
                    if damage > defeat_damage:
                        defeat_damage = damage
                        defeat_path = path
                        defeat_vertex = terminal_vertex
            else:
                paths_not_found += 1

        logger.info(f"[DIJKSTRA] Paths found: {paths_found}, Paths not found: {paths_not_found}")
        logger.info(f"[DIJKSTRA] Best victory path: {victory_path is not None}, Best defeat path: {defeat_path is not None}")
        if defeat_path:
            logger.info(f"[DIJKSTRA] Defeat path damage: {defeat_damage}, path length: {len(defeat_path)}")
        else:
            logger.warning(f"[DIJKSTRA] No defeat path found even though {defeat_count} defeat states exist!")

        # Choose best result: ONLY accept victory, never accept defeat!
        # (Defeat states are only used if NO victory is possible)
        if victory_path:
            best_path = victory_path
            best_terminal_vertex = victory_vertex
            best_distance = victory_distance
            logger.info(f"[DIJKSTRA] Found victory path! Distance: {victory_distance}, damage: {vertex_to_state.get(victory_vertex).get_total_damage_dealt_to_opponent()}")
        elif defeat_path:
            # Only use defeat path if no victory found (player too weak)
            logger.warning(f"[DIJKSTRA] No victory possible - using best defeat path with {defeat_damage} damage")
            best_path = defeat_path
            best_terminal_vertex = defeat_vertex
            best_distance = 0  # Doesn't matter for defeats
        else:
            best_path = None
            best_terminal_vertex = None
            best_distance = 0

        if best_path is None:
            # No path found (shouldn't happen)
            return DijkstraResult(
                success=False,
                total_damage=0,
                turns=0,
                move_sequence=[],
                final_state=initial_state,
                states_explored=graph.get_num_verts()
            )

        path = best_path

        # Extract move sequence from path (auto-switch handles Pokemon changes)
        move_sequence = []
        for i in range(len(path) - 1):
            from_vertex = path[i]
            to_vertex = path[i + 1]
            edge_key = (from_vertex, to_vertex)
            move_name = move_labels.get(edge_key)  # Just the move name
            if move_name:
                move_sequence.append(move_name)

        # Get final state
        final_state = vertex_to_state.get(best_terminal_vertex, initial_state)

        # Calculate statistics
        success = final_state.player_won()
        total_damage = final_state.get_total_damage_dealt_to_opponent()
        turns = len(move_sequence)

        return DijkstraResult(
            success=success,
            total_damage=total_damage,
            turns=turns,
            move_sequence=move_sequence,
            final_state=final_state,
            states_explored=graph.get_num_verts(),
            path_cost=best_distance
        )

    def _build_graph(
        self,
        initial_state: BattleState
    ) -> Tuple[Graph, Dict[str, int], Dict[int, BattleState], Dict[Tuple[int, int], str]]:
        """
        Build a battle state graph using BFS exploration.

        Args:
            initial_state: Starting battle state

        Returns:
            Tuple of:
            - Graph object
            - state_to_vertex: Maps state hash -> vertex ID
            - vertex_to_state: Maps vertex ID -> BattleState
            - move_labels: Maps (from_vertex, to_vertex) -> move name
        """
        graph = Graph()
        state_to_vertex: Dict[str, int] = {}
        vertex_to_state: Dict[int, BattleState] = {}
        move_labels: Dict[Tuple[int, int], str] = {}

        # Queue for BFS: (state, vertex_id)
        queue = []
        visited = set()

        # Add initial state
        initial_hash = initial_state.hash_key()
        initial_vertex_id = 0
        graph.add_vertex(Vertex(vertex_id=initial_vertex_id, name=initial_hash))
        state_to_vertex[initial_hash] = initial_vertex_id
        vertex_to_state[initial_vertex_id] = initial_state.copy()
        queue.append(initial_state.copy())
        visited.add(initial_hash)

        vertex_counter = 1

        # BFS to explore states
        while queue and vertex_counter < self.max_states:
            current_state = queue.pop(0)
            current_hash = current_state.hash_key()
            current_vertex_id = state_to_vertex[current_hash]

            # If this is a terminal state, don't explore further
            if current_state.is_battle_over():
                continue

            # Generate successors
            successors = current_state.generate_successor_states()

            for next_state, move, damage in successors:
                next_hash = next_state.hash_key()

                # Add vertex if not seen
                if next_hash not in state_to_vertex:
                    next_vertex_id = vertex_counter
                    graph.add_vertex(Vertex(vertex_id=next_vertex_id, name=next_hash))
                    state_to_vertex[next_hash] = next_vertex_id
                    vertex_to_state[next_vertex_id] = next_state.copy()
                    vertex_counter += 1

                    # Add to queue if not visited
                    if next_hash not in visited:
                        queue.append(next_state.copy())
                        visited.add(next_hash)
                else:
                    next_vertex_id = state_to_vertex[next_hash]

                # Add edge with weight = 1 turn (we want minimum turns)
                # Could also use: weight = 1 / (damage + 1) to prefer high damage
                weight = 1.0  # Each move costs 1 turn

                graph.add_directed_edge(
                    v1=current_vertex_id,
                    v2=next_vertex_id,
                    weight=weight
                )

                # Record move label (auto-switch handles Pokemon changes)
                move_labels[(current_vertex_id, next_vertex_id)] = move.name

        return graph, state_to_vertex, vertex_to_state, move_labels

    def _reconstruct_path(
        self,
        start: int,
        end: int,
        predecessors: List[Optional[int]]
    ) -> List[int]:
        """
        Reconstruct path from start to end using predecessor array.

        Args:
            start: Starting vertex ID
            end: Ending vertex ID
            predecessors: Predecessor array from Dijkstra

        Returns:
            List of vertex IDs forming the path
        """
        path = []
        current = end

        while current is not None:
            path.append(current)
            if current == start:
                break
            current = predecessors[current]

        path.reverse()
        return path


def run_dijkstra_optimizer(
    player_team: List[Pokemon],
    opponent_team: List[Pokemon],
    max_states: int = 100000
) -> DijkstraResult:
    """
    Convenience function to run Dijkstra optimizer on teams.

    Args:
        player_team: Player's Pokemon team
        opponent_team: Opponent's Pokemon team
        max_states: Maximum states to explore

    Returns:
        DijkstraResult with optimal strategy
    """
    initial_state = BattleState(
        player_team=player_team,
        opponent_team=opponent_team
    )

    optimizer = DijkstraBattleOptimizer(max_states=max_states)
    return optimizer.optimize(initial_state)
