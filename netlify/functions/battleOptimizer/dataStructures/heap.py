"""
Max Heap Data Structure - Converted from CS_311 Assignment 6

This module implements a max-heap (priority queue) with support for:
- Insert with O(log n) time complexity
- RemoveMax with O(log n) time complexity
- Heapify to build heap from array in O(n) time
- ChangeKey to update priorities

Original C++ implementation from:
- CS_311 Programming Assignment 6 (Heap & HeapSort)

Converted to Python for Pokemon Battle Optimizer Extra Credit Project
Used for: Greedy move selection (always pick highest damage move)

Author: Josh C.
Date: December 2025
"""

from typing import List, Optional, Any


class Heap:
    """
    Max-Heap implementation using array representation.

    A max-heap is a complete binary tree where each parent node has a value
    greater than or equal to its children. This property ensures the maximum
    element is always at the root.

    Array representation:
    - Parent of node i: (i - 1) // 2
    - Left child of node i: 2 * i + 1
    - Right child of node i: 2 * i + 2

    From Assignment 6: heap.h and heap.cpp
    """

    def __init__(self, capacity: int = 100, values: Optional[List[Any]] = None):
        """
        Constructor: Create a heap.

        Args:
            capacity: Initial capacity of the heap (default 100)
            values: Optional list of values to build heap from

        From Assignment 6: heap.cpp lines 15-46
        """
        if values is not None:
            # Build heap from array
            self.capacity = len(values)
            self.count = len(values)
            self.heaparray = values.copy()
            self.heapify()
        else:
            # Create empty heap
            self.capacity = capacity
            self.count = 0
            self.heaparray = [None] * capacity

    def size(self) -> int:
        """Return the number of elements in the heap."""
        return self.count

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return self.count == 0

    def left_child(self, index: int) -> int:
        """
        Get index of left child.

        Args:
            index: Index of parent node

        Returns:
            Index of left child

        From Assignment 6: heap.h lines 124-127
        """
        return 2 * index + 1

    def right_child(self, index: int) -> int:
        """
        Get index of right child.

        Args:
            index: Index of parent node

        Returns:
            Index of right child

        From Assignment 6: heap.h lines 131-134
        """
        return 2 * index + 2

    def parent(self, index: int) -> int:
        """
        Get index of parent node.

        Args:
            index: Index of child node

        Returns:
            Index of parent node, or -1 if invalid

        From Assignment 6: heap.h lines 139-144
        """
        if index <= 0 or index >= self.count:
            return -1
        return (index - 1) // 2

    def swap(self, index1: int, index2: int):
        """
        Swap values at two indices.

        Args:
            index1: First index
            index2: Second index

        From Assignment 6: heap.cpp lines 241-246
        """
        self.heaparray[index1], self.heaparray[index2] = \
            self.heaparray[index2], self.heaparray[index1]

    def percolate_down(self, index: int):
        """
        Percolate node down to maintain max-heap property.

        Recursively swaps the node at index with its larger child
        until heap property is restored.

        Args:
            index: Index of node to percolate down

        From Assignment 6: heap.cpp lines 108-132
        """
        # Check if index is valid
        if index < 0 or index >= self.count:
            return

        left = self.left_child(index)
        right = self.right_child(index)
        largest = index

        # Find the largest among node, left child, and right child
        if left < self.count and self.heaparray[left] > self.heaparray[largest]:
            largest = left

        if right < self.count and self.heaparray[right] > self.heaparray[largest]:
            largest = right

        # If largest is not the current node, swap and continue
        if largest != index:
            self.swap(index, largest)
            self.percolate_down(largest)

    def percolate_up(self, index: int):
        """
        Percolate node up to maintain max-heap property.

        Recursively swaps the node at index with its parent
        until heap property is restored.

        Args:
            index: Index of node to percolate up

        From Assignment 6: heap.cpp lines 137-150
        """
        # Check if we're at root or invalid index
        if index <= 0 or index >= self.count:
            return

        parent_index = self.parent(index)

        # If current node is greater than parent, swap and continue
        if parent_index >= 0 and self.heaparray[index] > self.heaparray[parent_index]:
            self.swap(index, parent_index)
            self.percolate_up(parent_index)

    def heapify(self):
        """
        Reorganize array into a valid max-heap.

        Starts from the last non-leaf node and percolates down.
        This builds a heap in O(n) time.

        From Assignment 6: heap.cpp lines 97-103
        """
        # Start from last non-leaf node and percolate down
        # Last non-leaf node is at index (count // 2 - 1)
        for i in range(self.count // 2 - 1, -1, -1):
            self.percolate_down(i)

    def insert(self, value: Any):
        """
        Insert a value into the heap.

        Adds value at the end and percolates up to maintain heap property.
        Automatically resizes if capacity is reached.

        Args:
            value: Value to insert

        Complexity: O(log n)

        From Assignment 6: heap.cpp lines 156-180
        """
        # Check if we need to resize
        if self.count >= self.capacity:
            # Double the capacity
            new_capacity = self.capacity * 2
            new_array = [None] * new_capacity

            # Copy existing elements
            for i in range(self.count):
                new_array[i] = self.heaparray[i]

            self.heaparray = new_array
            self.capacity = new_capacity

        # Insert new value at the end
        self.heaparray[self.count] = value
        self.count += 1

        # Percolate up to maintain heap property
        self.percolate_up(self.count - 1)

    def get_max(self) -> Optional[Any]:
        """
        Get the maximum value without removing it.

        Returns:
            Maximum value in the heap, or None if empty

        Complexity: O(1)

        From Assignment 6: heap.cpp lines 5-11
        """
        if self.count == 0:
            return None
        return self.heaparray[0]

    def remove_max(self) -> Optional[Any]:
        """
        Remove and return the maximum value from the heap.

        Replaces root with last element and percolates down.

        Returns:
            Maximum value that was removed, or None if empty

        Complexity: O(log n)

        From Assignment 6: heap.cpp lines 186-205
        """
        # Check if heap is empty
        if self.count == 0:
            return None

        # Store the max value (root)
        max_value = self.heaparray[0]

        # Move last element to root
        self.heaparray[0] = self.heaparray[self.count - 1]
        self.count -= 1

        # Percolate down to maintain heap property
        if self.count > 0:
            self.percolate_down(0)

        return max_value

    def change_key(self, index: int, new_val: Any):
        """
        Change the value at a specific index and restore heap property.

        Args:
            index: Index of element to change
            new_val: New value for the element

        From Assignment 6: heap.cpp lines 276-296
        """
        # Check if index is valid
        if index < 0 or index >= self.count:
            return

        # Store old value
        old_value = self.heaparray[index]

        # Change the value
        self.heaparray[index] = new_val

        # If new value is greater, percolate up
        # If new value is smaller, percolate down
        if new_val > old_value:
            self.percolate_up(index)
        elif new_val < old_value:
            self.percolate_down(index)
        # If equal, no need to do anything

    def to_list(self) -> List[Any]:
        """Return heap contents as a list (level-order)."""
        return self.heaparray[:self.count]

    def __str__(self) -> str:
        """String representation of the heap."""
        return f"Heap({self.to_list()})"

    def __repr__(self) -> str:
        return f"Heap(size={self.count}, capacity={self.capacity}, max={self.get_max()})"


def heap_sort(values: List[Any]) -> List[Any]:
    """
    Sort an array using heap sort algorithm.

    Creates a max-heap from the array, then repeatedly extracts the maximum
    element to build a sorted array.

    Args:
        values: List of values to sort

    Returns:
        Sorted list in ascending order

    Complexity: O(n log n)

    From Assignment 6: heap.cpp lines 251-268
    """
    if not values:
        return []

    # Create a heap from the array
    heap = Heap(values=values)

    # Extract elements from heap one by one in descending order
    # Place them back in array in ascending order (reversed)
    result = []
    for _ in range(len(values)):
        result.append(heap.remove_max())

    # Reverse to get ascending order
    result.reverse()

    return result


# ============================================================================
# Testing code (run with: python heap.py)
# ============================================================================

if __name__ == "__main__":
    print("Testing Heap Implementation (from CS_311 Assignment 6)")
    print("=" * 60)

    # Test 1: Basic insert and removeMax
    print("\n=== Test 1: Insert and RemoveMax ===")
    heap = Heap()
    values = [45, 20, 14, 12, 31, 7, 11, 13, 7]

    print(f"Inserting values: {values}")
    for val in values:
        heap.insert(val)

    print(f"Heap after insertions: {heap}")
    print(f"Max value: {heap.get_max()}")

    print("\nRemoving max values:")
    while not heap.is_empty():
        max_val = heap.remove_max()
        print(f"  Removed: {max_val}, Remaining: {heap.to_list()}")

    # Test 2: Build heap from array (heapify)
    print("\n=== Test 2: Heapify (Build from Array) ===")
    arr = [3, 9, 2, 1, 4, 5]
    print(f"Original array: {arr}")
    heap2 = Heap(values=arr)
    print(f"After heapify: {heap2.to_list()}")
    print(f"Max: {heap2.get_max()}")

    # Test 3: Heap sort
    print("\n=== Test 3: Heap Sort ===")
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    print(f"Unsorted: {unsorted}")
    sorted_arr = heap_sort(unsorted)
    print(f"Sorted:   {sorted_arr}")

    # Test 4: Change key
    print("\n=== Test 4: Change Key ===")
    heap3 = Heap(values=[10, 20, 30, 40, 50])
    print(f"Original heap: {heap3.to_list()}")
    print(f"Max: {heap3.get_max()}")

    print("Changing index 2 from 30 to 100...")
    heap3.change_key(2, 100)
    print(f"After change: {heap3.to_list()}")
    print(f"New max: {heap3.get_max()}")

    # Test 5: Use for greedy algorithm simulation
    print("\n=== Test 5: Greedy Move Selection (Pokemon Example) ===")

    # Simulate moves with damage values
    moves = [
        ("Thunderbolt", 95),
        ("Quick Attack", 40),
        ("Thunder", 110),
        ("Tackle", 35),
    ]

    move_heap = Heap()
    print("Pokemon moves:")
    for name, damage in moves:
        print(f"  {name}: {damage} damage")
        move_heap.insert((damage, name))  # Insert tuple (damage, name)

    print("\nGreedy selection (always pick highest damage):")
    while not move_heap.is_empty():
        damage, name = move_heap.remove_max()
        print(f"  Use {name} ({damage} damage)")

    print("\n" + "=" * 60)
    print("✅ Heap implementation complete!")
    print("From CS_311 Assignment 6 (Heap & HeapSort)")
    print("Ready for Greedy Battle Optimizer!")
