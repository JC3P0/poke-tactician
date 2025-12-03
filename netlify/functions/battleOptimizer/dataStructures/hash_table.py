"""
Hash Table Data Structure - Converted from CS_311 Assignment 7

This module implements a hash table with separate chaining for collision resolution:
- Insert with O(1) average time complexity
- Find/Get with O(1) average time complexity
- Remove with O(1) average time complexity
- Rehash to resize when load factor exceeds threshold

Original C++ implementation from:
- CS_311 Programming Assignment 7 (Hash Tables)

Converted to Python for Pokemon Battle Optimizer Extra Credit Project
Used for: Dynamic Programming memoization cache

Author: Josh C.
Date: December 2025
"""

from typing import Any, Optional, List, Tuple


class Node:
    """
    Node class for linked list (separate chaining).

    Attributes:
        key: Key for the hash table entry
        value: Value associated with the key
        next: Pointer to next node in the chain

    From Assignment 7: linkedlist.h lines 20-29
    """
    def __init__(self, key: Any, value: Any, next_node: Optional['Node'] = None):
        self.key = key
        self.value = value
        self.next = next_node


class LinkedList:
    """
    Singly linked list for separate chaining in hash table.

    Simplified version of Assignment 7's LinkedList, adapted for key-value pairs
    instead of Order objects.

    From Assignment 7: linkedlist.h
    """
    def __init__(self):
        """Create an empty linked list."""
        self.front: Optional[Node] = None
        self.rear: Optional[Node] = None
        self.count = 0

    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self.count == 0

    def length(self) -> int:
        """Return the number of nodes in the list."""
        return self.count

    def add_rear(self, key: Any, value: Any):
        """
        Add a new node at the rear of the list.

        Args:
            key: Key for the entry
            value: Value for the entry

        From Assignment 7: linkedlist.cpp addRear()
        """
        new_node = Node(key, value)

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self.count += 1

    def search(self, key: Any) -> int:
        """
        Search for a key in the list.

        Args:
            key: Key to search for

        Returns:
            Position of the key (0-indexed), or -1 if not found

        From Assignment 7: linkedlist.cpp search()
        """
        current = self.front
        pos = 0

        while current is not None:
            if current.key == key:
                return pos
            current = current.next
            pos += 1

        return -1

    def get_node(self, pos: int) -> Optional[Node]:
        """
        Get the node at a given position.

        Args:
            pos: Position (0-indexed)

        Returns:
            Node at position, or None if out of range

        From Assignment 7: linkedlist.h lines 125-134
        """
        if pos < 0 or pos >= self.count:
            return None

        current = self.front
        for _ in range(pos):
            current = current.next

        return current

    def delete_at(self, pos: int) -> Tuple[bool, Optional[Any], Optional[Any]]:
        """
        Delete node at given position.

        Args:
            pos: Position to delete (0-indexed)

        Returns:
            Tuple of (success, deleted_key, deleted_value)

        From Assignment 7: linkedlist.cpp deleteAt()
        """
        if pos < 0 or pos >= self.count:
            return False, None, None

        # Delete at front
        if pos == 0:
            deleted_node = self.front
            self.front = self.front.next

            if self.count == 1:
                self.rear = None

            self.count -= 1
            return True, deleted_node.key, deleted_node.value

        # Delete at middle or rear
        prev = self.front
        for _ in range(pos - 1):
            prev = prev.next

        deleted_node = prev.next
        prev.next = deleted_node.next

        # Update rear if we deleted the last node
        if deleted_node == self.rear:
            self.rear = prev

        self.count -= 1
        return True, deleted_node.key, deleted_node.value

    def get_all_entries(self) -> List[Tuple[Any, Any]]:
        """
        Get all key-value pairs in the list.

        Returns:
            List of (key, value) tuples
        """
        entries = []
        current = self.front

        while current is not None:
            entries.append((current.key, current.value))
            current = current.next

        return entries


class HashTable:
    """
    Hash Table implementation using separate chaining.

    Uses an array of linked lists to handle collisions.
    Automatically rehashes when load factor exceeds 0.75.

    From Assignment 7: htable.h and htable.cpp
    """

    def __init__(self, size: int = 23):
        """
        Constructor: Create an empty hash table.

        Args:
            size: Number of buckets (default 23, a prime number)

        From Assignment 7: htable.cpp lines 13-17
        """
        self.table_size = size
        self.table: List[LinkedList] = []
        self.num_entries = 0

        # Create buckets
        for _ in range(size):
            self.table.append(LinkedList())

    def hash(self, key: Any) -> int:
        """
        Hash function to map a key to a bucket index.

        Args:
            key: Key to hash (can be int, str, or any hashable type)

        Returns:
            Bucket index (0 to table_size - 1)

        From Assignment 7: htable.cpp lines 31-34
        """
        # Use Python's built-in hash function, then mod by table size
        return hash(key) % self.table_size

    def insert(self, key: Any, value: Any) -> bool:
        """
        Insert a key-value pair into the hash table.
        Entry is inserted only if the key doesn't already exist.

        Args:
            key: Key for the entry
            value: Value for the entry

        Returns:
            True if inserted, False if key already exists

        Complexity: O(1) average case

        From Assignment 7: htable.cpp lines 68-83
        """
        # Check if key already exists
        if self.contains(key):
            return False

        # Get the bucket index
        index = self.hash(key)

        # Add to the linked list at this bucket
        self.table[index].add_rear(key, value)
        self.num_entries += 1

        # Check if we need to rehash (load factor > 0.75)
        if self.load_factor() > 0.75:
            self.rehash(self.table_size * 2)

        return True

    def get(self, key: Any) -> Optional[Any]:
        """
        Get the value associated with a key.

        Args:
            key: Key to search for

        Returns:
            Value if found, None otherwise

        Complexity: O(1) average case

        From Assignment 7: htable.cpp lines 42-61 (findOrder)
        """
        index = self.hash(key)

        # Search the linked list at this bucket
        pos = self.table[index].search(key)

        if pos >= 0:
            node = self.table[index].get_node(pos)
            return node.value

        return None

    def contains(self, key: Any) -> bool:
        """
        Check if a key exists in the hash table.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise

        Complexity: O(1) average case
        """
        index = self.hash(key)
        return self.table[index].search(key) >= 0

    def remove(self, key: Any) -> bool:
        """
        Remove a key-value pair from the hash table.

        Args:
            key: Key to remove

        Returns:
            True if removed, False if key doesn't exist

        Complexity: O(1) average case

        From Assignment 7: htable.cpp lines 115-133
        """
        index = self.hash(key)

        # Search for the key in the linked list
        pos = self.table[index].search(key)

        if pos >= 0:
            # Delete the entry at this position
            success, _, _ = self.table[index].delete_at(pos)
            if success:
                self.num_entries -= 1
                return True

        return False

    def update(self, key: Any, value: Any) -> bool:
        """
        Update the value for an existing key.
        Only updates if the key exists.

        Args:
            key: Key to update
            value: New value

        Returns:
            True if updated, False if key doesn't exist

        From Assignment 7: htable.cpp lines 164-182
        """
        index = self.hash(key)

        # Search for the key
        pos = self.table[index].search(key)

        if pos >= 0:
            node = self.table[index].get_node(pos)
            node.value = value
            return True

        return False

    def set(self, key: Any, value: Any):
        """
        Set a key-value pair (insert if new, update if exists).

        Args:
            key: Key to set
            value: Value to set
        """
        if not self.update(key, value):
            self.insert(key, value)

    def size(self) -> int:
        """
        Get the number of entries in the hash table.

        Returns:
            Number of key-value pairs

        From Assignment 7: htable.cpp lines 148-155
        """
        return self.num_entries

    def num_buckets(self) -> int:
        """
        Get the number of buckets in the hash table.

        Returns:
            Number of buckets

        From Assignment 7: htable.h lines 91-93
        """
        return self.table_size

    def load_factor(self) -> float:
        """
        Calculate the load factor (entries per bucket).

        Returns:
            Load factor (num_entries / table_size)
        """
        return self.num_entries / self.table_size if self.table_size > 0 else 0

    def rehash(self, new_size: int):
        """
        Rehash the table to a new size.
        Collects all entries and re-inserts them into a new table.

        Args:
            new_size: New number of buckets

        Complexity: O(n) where n is number of entries

        From Assignment 7: htable.cpp lines 189-210
        """
        # Step 1: Collect all entries from current table
        all_entries: List[Tuple[Any, Any]] = []

        for i in range(self.table_size):
            entries = self.table[i].get_all_entries()
            all_entries.extend(entries)

        # Step 2: Clear current table and resize
        self.table.clear()
        self.table_size = new_size
        self.num_entries = 0

        # Create new buckets
        for _ in range(new_size):
            self.table.append(LinkedList())

        # Step 3: Re-insert all entries
        for key, value in all_entries:
            self.insert(key, value)

    def print_table(self):
        """
        Print the hash table structure (for debugging).

        From Assignment 7: htable.cpp lines 136-141
        """
        print(f"Hash Table (size={self.table_size}, entries={self.num_entries}, load={self.load_factor():.2f}):")
        for i in range(self.table_size):
            if not self.table[i].is_empty():
                print(f"  Bucket {i}: ", end="")
                entries = self.table[i].get_all_entries()
                for key, value in entries:
                    print(f"({key}: {value}) ", end="")
                print()
        print()

    def __repr__(self):
        return f"HashTable(size={self.table_size}, entries={self.num_entries}, load={self.load_factor():.2f})"


# ============================================================================
# Testing code (run with: python hash_table.py)
# ============================================================================

if __name__ == "__main__":
    print("Testing Hash Table Implementation (from CS_311 Assignment 7)")
    print("=" * 60)

    # Test 1: Basic insert and get
    print("\n=== Test 1: Insert and Get ===")
    ht = HashTable(7)  # Small table to test collisions

    # Insert some key-value pairs
    entries = [
        (101, "Pikachu"),
        (25, "Charizard"),
        (150, "Mewtwo"),
        (1, "Bulbasaur"),
        (94, "Gengar"),
    ]

    print("Inserting Pokemon:")
    for id, name in entries:
        result = ht.insert(id, name)
        print(f"  Insert({id}, '{name}'): {result}")

    print(f"\nHash table: {ht}")

    print("\nRetrieving Pokemon:")
    for id, expected_name in entries:
        name = ht.get(id)
        print(f"  Get({id}): {name}")

    # Test 2: Collision handling
    print("\n=== Test 2: Collision Handling ===")
    ht.print_table()

    # Test 3: Update
    print("=== Test 3: Update ===")
    print(f"Before update: Get(25) = {ht.get(25)}")
    ht.update(25, "Charmander")
    print(f"After update: Get(25) = {ht.get(25)}")

    # Test 4: Remove
    print("\n=== Test 4: Remove ===")
    print(f"Before remove: Contains(150) = {ht.contains(150)}")
    ht.remove(150)
    print(f"After remove: Contains(150) = {ht.contains(150)}")
    print(f"Get(150) = {ht.get(150)}")

    # Test 5: Rehashing (automatic when load factor > 0.75)
    print("\n=== Test 5: Automatic Rehashing ===")
    ht2 = HashTable(3)  # Very small table
    print(f"Initial: {ht2}")

    for i in range(10):
        ht2.insert(i, f"Pokemon_{i}")
        print(f"After insert {i}: {ht2}")

    # Test 6: Memoization use case (DP cache)
    print("\n=== Test 6: DP Memoization Cache ===")
    memo = HashTable(23)

    # Simulate battle state caching
    # Key: battle state string, Value: optimal damage
    battle_states = [
        ("Pikachu_100HP_vs_Onix_80HP", 450),
        ("Charizard_120HP_vs_Blastoise_100HP", 680),
        ("Mewtwo_150HP_vs_Mew_150HP", 920),
    ]

    print("Caching battle state results:")
    for state, damage in battle_states:
        memo.insert(state, damage)
        print(f"  Cached: {state} -> {damage} damage")

    print("\nRetrieving cached results:")
    for state, expected_damage in battle_states:
        damage = memo.get(state)
        cache_hit = "HIT" if damage is not None else "MISS"
        print(f"  [{cache_hit}] {state} -> {damage} damage")

    # Test cache miss
    print("\nTesting cache miss:")
    result = memo.get("Alakazam_vs_Machamp")
    print(f"  Get('Alakazam_vs_Machamp'): {result} (cache miss)")

    print("\n" + "=" * 60)
    print("✅ Hash Table implementation complete!")
    print("From CS_311 Assignment 7 (Hash Tables with Separate Chaining)")
    print("Ready for Dynamic Programming Memoization!")
