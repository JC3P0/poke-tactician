"""
Pokemon Data Service - Facade for Pokemon data conversion

This service handles conversion between MongoDB Pokemon data and
our battle optimizer Pokemon objects.

Architecture Pattern: Facade
- Abstracts complexity of data conversion
- Provides simple interface for frontend/backend integration
- Handles edge cases and defaults

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os
from typing import Dict, List, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pokemon import Pokemon
from models.move import Move
from data.gen1Moves import get_move_by_name, get_random_moves_for_pokemon


class PokemonDataService:
    """
    Facade for converting MongoDB Pokemon data to battle-ready Pokemon objects.

    This service handles:
    - MongoDB format → Pokemon class conversion
    - Move selection and conversion
    - Default values (DVs, levels)
    - Error handling
    """

    @staticmethod
    def from_mongodb(data: Dict[str, Any], level: int = 50, move_names: Optional[List[str]] = None, dvs: Optional[Dict[str, int]] = None) -> Pokemon:
        """
        Convert MongoDB Pokemon data to a Pokemon object.

        Expected MongoDB format (from getGen1Pokemon):
        {
          "id": 25,
          "name": "pikachu",
          "types": ["electric"],
          "base_stats": {
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special": 50,
            "speed": 90
          },
          "moves": ["thunderbolt", "thunder-wave", "quick-attack", "thunder"]
        }

        Args:
            data: MongoDB Pokemon data dictionary
            level: Pokemon level (default 50)
            move_names: Optional list of specific moves to use (max 4)
                       If None, automatically selects best damaging moves

        Returns:
            Pokemon object ready for battle

        Raises:
            KeyError: If required data is missing
            ValueError: If data is invalid
        """
        # Validate required fields
        if 'name' not in data:
            raise KeyError("Pokemon data missing 'name' field")
        if 'types' not in data:
            raise KeyError("Pokemon data missing 'types' field")
        if 'base_stats' not in data:
            raise KeyError("Pokemon data missing 'base_stats' field")

        name = data['name'].capitalize()
        types = [t.capitalize() for t in data['types']]

        # Extract base stats
        base_stats_raw = data['base_stats']
        base_stats = {
            "HP": base_stats_raw.get('hp', 50),
            "Attack": base_stats_raw.get('attack', 50),
            "Defense": base_stats_raw.get('defense', 50),
            "Speed": base_stats_raw.get('speed', 50),
            "Special": base_stats_raw.get('special', 50)
        }

        # Use custom DVs if provided, otherwise default to max (15)
        if dvs is None:
            dvs = {
                "HP": 15,
                "Attack": 15,
                "Defense": 15,
                "Speed": 15,
                "Special": 15
            }
        else:
            # Ensure all required stats are present
            default_dvs = {"HP": 15, "Attack": 15, "Defense": 15, "Speed": 15, "Special": 15}
            for stat in default_dvs:
                if stat not in dvs:
                    dvs[stat] = default_dvs[stat]

        # Handle moves
        available_moves = data.get('moves', [])

        if move_names:
            # Use specified moves
            moves = []
            for move_name in move_names[:4]:  # Max 4 moves
                try:
                    moves.append(get_move_by_name(move_name))
                except KeyError:
                    # Skip unknown moves
                    continue
        else:
            # Auto-select best moves
            moves = get_random_moves_for_pokemon(available_moves, count=4)

        # Ensure we have at least one move
        if not moves:
            moves = [Move("Tackle", "Normal", 35, 95, 35)]

        # Create Pokemon object
        return Pokemon(
            name=name,
            types=types,
            level=level,
            base_stats=base_stats,
            dvs=dvs,
            moves=moves
        )

    @staticmethod
    def from_mongodb_list(data_list: List[Dict[str, Any]], level: int = 50) -> List[Pokemon]:
        """
        Convert a list of MongoDB Pokemon to Pokemon objects.

        Args:
            data_list: List of MongoDB Pokemon data dictionaries
            level: Default Pokemon level (used if individual Pokemon doesn't specify)

        Returns:
            List of Pokemon objects
        """
        pokemon_list = []
        for data in data_list:
            # Use individual Pokemon's level if provided, otherwise use default
            poke_level = data.get('level', level)

            # Use individual Pokemon's DVs if provided
            poke_dvs = data.get('dvs', None)

            # Use individual Pokemon's selected moves if provided
            move_names = data.get('selectedMoves', data.get('moves', None))

            pokemon_list.append(
                PokemonDataService.from_mongodb(
                    data,
                    level=poke_level,
                    move_names=move_names,
                    dvs=poke_dvs
                )
            )

        return pokemon_list

    @staticmethod
    def to_api_response(pokemon: Pokemon) -> Dict[str, Any]:
        """
        Convert a Pokemon object back to API response format.

        Args:
            pokemon: Pokemon object

        Returns:
            Dictionary suitable for JSON response
        """
        return pokemon.to_dict()
