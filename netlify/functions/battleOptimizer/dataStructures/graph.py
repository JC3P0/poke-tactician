"""
Graph Data Structure - Converted from CS_311 Assignment 8 & 9

This module implements a directed/undirected graph with support for:
- BFS (Breadth-First Search) - Assignment 8
- DFS (Depth-First Search) - Assignment 8
- Dijkstra's Shortest Path Algorithm - Assignment 9
- Cycle Detection - Assignment 8

Original C++ implementation from:
- CS_311 Programming Assignment 8 (Graph Traversal)
- CS_311 Programming Assignment 9 (Shortest Path)

Converted to Python for Pokemon Battle Optimizer Extra Credit Project
Author: Josh C.
Date: December 2025
"""

from typing import List, Tuple, Optional
from collections import deque
import heapq
import sys


class Vertex:
    """
    Vertex class representing a node in the graph.

    Attributes:
        id: Unique identifier for the vertex (int)
        name: Optional name for the vertex (str)

    From Assignment 8: graph.h lines 16-27
    """
    def __init__(self, vertex_id: int = 0, name: str = ""):
        self.id = vertex_id
        self.name = name

    def __repr__(self):
        return f"Vertex(id={self.id}, name='{self.name}')"


class Edge:
    """
    Edge class representing a directed edge from one vertex to another.

    Attributes:
        from_vertex: Index of the starting vertex (int)
        to_vertex: Index of the ending vertex (int)
        weight: Weight/cost of the edge (float)

    From Assignment 8: graph.h lines 33-43
    """
    def __init__(self, from_vertex: int = 0, to_vertex: int = 0, weight: float = 1.0):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __repr__(self):
        return f"Edge({self.from_vertex} -> {self.to_vertex}, weight={self.weight})"


class Graph:
    """
    Graph class implementing an adjacency list representation.

    Supports both directed and undirected graphs.
    Implements BFS, DFS, and Dijkstra's shortest path algorithm.

    From Assignment 8 & 9: graph.h and graph.cpp
    """

    def __init__(self, num_vertices: int = 0):
        """
        Constructor: Create a graph with specified number of vertices.

        Args:
            num_vertices: Initial number of vertices in the graph

        From Assignment 8: graph.cpp lines 5-16
        """
        self.num_verts = num_vertices
        self.vertices: List[Vertex] = []
        self.adj_list: List[List[Edge]] = []

        # Initialize with default vertices
        for i in range(num_vertices):
            self.vertices.append(Vertex(i))
            self.adj_list.append([])

    def get_num_verts(self) -> int:
        """Return the number of vertices in the graph."""
        return self.num_verts

    def add_vertex(self, vertex: Vertex):
        """
        Add a new vertex to the graph.

        Args:
            vertex: Vertex object to add

        From Assignment 8: graph.cpp lines 25-30
        """
        self.vertices.append(vertex)
        self.adj_list.append([])
        self.num_verts += 1

    def add_directed_edge(self, v1: int, v2: int, weight: float = 1.0):
        """
        Add a directed edge from v1 to v2.

        Args:
            v1: Index of the starting vertex
            v2: Index of the ending vertex
            weight: Weight of the edge (default 1.0)

        From Assignment 8: graph.cpp lines 33-37
        """
        edge = Edge(v1, v2, weight)
        self.adj_list[v1].append(edge)

    def add_undirected_edge(self, v1: int, v2: int, weight: float = 1.0):
        """
        Add an undirected edge between v1 and v2.
        Implemented as two directed edges.

        Args:
            v1: Index of the first vertex
            v2: Index of the second vertex
            weight: Weight of the edge (default 1.0)

        From Assignment 8: graph.cpp lines 40-44
        """
        self.add_directed_edge(v1, v2, weight)
        self.add_directed_edge(v2, v1, weight)

    def out_degree(self, v: int) -> int:
        """
        Get the number of outgoing edges from a vertex.

        Args:
            v: Index of the vertex

        Returns:
            Number of outgoing edges

        From Assignment 8: graph.cpp lines 47-50
        """
        return len(self.adj_list[v])

    def depth_first_search(self, start: int) -> List[int]:
        """
        Perform Depth-First Search starting from a vertex.
        Uses an iterative approach with a stack.

        Args:
            start: Index of the starting vertex

        Returns:
            List of vertex indices in the order they were visited

        From Assignment 8: graph.cpp lines 53-89
        """
        result = []
        visited = [False] * self.num_verts
        stack = [start]

        while stack:
            current = stack.pop()  # Pop from end (stack behavior)

            if not visited[current]:
                visited[current] = True
                result.append(current)

                # Push neighbors in reverse order to maintain traversal order
                neighbors = []
                for edge in self.adj_list[current]:
                    if not visited[edge.to_vertex]:
                        neighbors.append(edge.to_vertex)

                # Push in reverse to maintain order
                for neighbor in reversed(neighbors):
                    stack.append(neighbor)

        return result

    def breadth_first_search(self, start: int) -> List[int]:
        """
        Perform Breadth-First Search starting from a vertex.
        Uses a queue for level-by-level traversal.

        Args:
            start: Index of the starting vertex

        Returns:
            List of vertex indices in the order they were visited

        From Assignment 8: graph.cpp lines 92-125
        """
        result = []
        visited = [False] * self.num_verts
        queue = deque([start])
        visited[start] = True

        while queue:
            current = queue.popleft()  # Dequeue from front
            result.append(current)

            # Enqueue all unvisited neighbors
            for edge in self.adj_list[current]:
                neighbor = edge.to_vertex
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

        return result

    def check_cycle(self) -> bool:
        """
        Check if the undirected graph contains cycles.
        Uses DFS with parent tracking.

        Returns:
            True if graph contains at least one cycle, False otherwise

        From Assignment 8: graph.cpp lines 157-171
        """
        visited = [False] * self.num_verts

        def check_cycle_util(v: int, parent: int) -> bool:
            """Helper function for cycle detection using DFS."""
            visited[v] = True

            for edge in self.adj_list[v]:
                neighbor = edge.to_vertex

                if not visited[neighbor]:
                    if check_cycle_util(neighbor, v):
                        return True
                elif neighbor != parent:
                    # Found a cycle (visited neighbor that's not parent)
                    return True

            return False

        # Check each connected component
        for i in range(self.num_verts):
            if not visited[i]:
                if check_cycle_util(i, -1):
                    return True

        return False

    def dijkstra(self, source: int, dest: int) -> Tuple[Optional[int], Optional[List[int]]]:
        """
        Find shortest path from source to destination using Dijkstra's algorithm.
        Uses a priority queue (min-heap) for efficient vertex selection.

        Args:
            source: Index of the starting vertex
            dest: Index of the destination vertex

        Returns:
            Tuple of (distance, path):
                - distance: Total distance from source to dest (None if no path)
                - path: List of vertex indices along the shortest path (None if no path)

        Complexity: O((V + E) log V) with binary heap

        From Assignment 9: graph.cpp lines 200-261
        """
        INF = sys.maxsize

        # Initialize distances and tracking arrays
        dist = [INF] * self.num_verts
        previous = [-1] * self.num_verts
        visited = [False] * self.num_verts

        dist[source] = 0

        # Priority queue: (distance, vertex_index)
        # Python heapq is a min-heap by default
        pq = [(0, source)]

        while pq:
            # Get vertex with minimum distance
            current_dist, u = heapq.heappop(pq)

            # Skip if already visited
            if visited[u]:
                continue
            visited[u] = True

            # Early exit if we reached destination
            if u == dest:
                break

            # Check all neighbors of u
            for edge in self.adj_list[u]:
                v = edge.to_vertex
                weight = int(edge.weight)

                # Relaxation step: found shorter path to v through u
                if not visited[v] and dist[u] != INF and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    previous[v] = u
                    heapq.heappush(pq, (dist[v], v))

        # Check if destination is reachable
        if dist[dest] == INF:
            return None, None  # No path exists

        # Reconstruct path from source to dest
        path = []
        current = dest
        while current != -1:
            path.append(current)
            current = previous[current]
        path.reverse()

        return dist[dest], path

    def print_graph(self):
        """
        Print the graph structure (for debugging).

        From Assignment 8: graph.cpp lines 174-188
        """
        print("Graph:")
        for i in range(self.num_verts):
            print(f"{i}: ", end="")
            for edge in self.adj_list[i]:
                print(f"{edge.to_vertex}(w={edge.weight}) ", end="")
            print()
        print()

    def __repr__(self):
        return f"Graph(vertices={self.num_verts}, edges={sum(len(adj) for adj in self.adj_list)})"


# ============================================================================
# Testing code (run with: python graph.py)
# ============================================================================

if __name__ == "__main__":
    print("Testing Graph Implementation (from CS_311 Assignments 8 & 9)")
    print("=" * 60)

    # Create a simple test graph
    #     0
    #    / \
    #   1   2
    #    \ /
    #     3
    g = Graph(4)
    g.add_undirected_edge(0, 1, 1)
    g.add_undirected_edge(0, 2, 2)
    g.add_undirected_edge(1, 3, 3)
    g.add_undirected_edge(2, 3, 1)

    print("\nTest Graph:")
    g.print_graph()

    print("\nBFS from vertex 0:")
    print(g.breadth_first_search(0))

    print("\nDFS from vertex 0:")
    print(g.depth_first_search(0))

    print("\nShortest path from 0 to 3 (Dijkstra):")
    distance, path = g.dijkstra(0, 3)
    if path:
        print(f"Distance: {distance}")
        print(f"Path: {' -> '.join(map(str, path))}")
    else:
        print("No path found")

    print("\nCheck for cycles:")
    print(f"Has cycle: {g.check_cycle()}")

    print("\n" + "=" * 60)
    print("✅ Graph implementation complete!")
    print("From CS_311 Assignment 8 (BFS/DFS) and Assignment 9 (Dijkstra)")
