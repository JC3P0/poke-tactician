"""
Pokemon Battle Optimizer - Netlify Serverless Function
CS_311 Extra Credit Project

This serverless function implements a Pokemon Gen 1 battle optimizer using
data structures and algorithms from CS_311 assignments.

Data Structures Used:
- Graph (Assignment 8 & 9): Battle state space representation + Dijkstra
- Hash Table (Assignment 7): Memoization cache for DP
- Heap (Assignment 6): Priority queue for Greedy move selection

Author: Josh C.
Date: December 2025
"""

import json
import sys
import os
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.pokemon import Pokemon
from models.battleState import BattleState
from algorithms.greedy import run_greedy_optimizer
from algorithms.dynamic_programming import run_dp_optimizer
from algorithms.dijkstra import run_dijkstra_optimizer
from data.bossTrainers import get_boss_trainer


def handler(event, context):
    """
    Netlify serverless function handler.

    Expected POST body:
    {
        "playerTeam": [Pokemon objects with name, level, types, base_stats, dvs, moves],
        "opponentTeam": [Pokemon objects] OR "bossTrainer": "blue" | "giovanni" | "lance",
        "algorithm": "greedy" | "dp" | "dijkstra" (default: "dijkstra")
    }

    Returns:
    {
        "success": true,
        "algorithm": "dijkstra",
        "result": {
            "success": true,
            "totalDamage": 500,
            "turns": 5,
            "moveSequence": ["Thunderbolt", "Thunder", ...],
            "statesExplored": 150 (dijkstra only),
            "cacheHitRate": 0.54 (dp only)
        }
    }
    """

    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))

        player_team_data = body.get('playerTeam', [])
        algorithm = body.get('algorithm', 'dijkstra').lower()

        # Validate algorithm
        if algorithm not in ['greedy', 'dp', 'dijkstra']:
            return error_response(f'Invalid algorithm: {algorithm}. Must be greedy, dp, or dijkstra.', 400)

        # Validate player team
        if not player_team_data:
            return error_response('Missing player team data', 400)

        # Build player team
        player_team = []
        for pkmn_data in player_team_data:
            try:
                player_team.append(Pokemon.from_dict(pkmn_data))
            except Exception as e:
                return error_response(f'Invalid Pokemon data: {str(e)}', 400)

        # Get opponent team (either custom or boss trainer)
        opponent_team = []
        if 'bossTrainer' in body:
            boss_id = body['bossTrainer']
            try:
                boss_data = get_boss_trainer(boss_id)
                opponent_team = boss_data['team']
            except ValueError as e:
                return error_response(str(e), 400)
        elif 'opponentTeam' in body:
            opponent_team_data = body['opponentTeam']
            for pkmn_data in opponent_team_data:
                try:
                    opponent_team.append(Pokemon.from_dict(pkmn_data))
                except Exception as e:
                    return error_response(f'Invalid opponent Pokemon data: {str(e)}', 400)
        else:
            return error_response('Must provide either opponentTeam or bossTrainer', 400)

        # Run the selected algorithm
        if algorithm == 'greedy':
            result = run_greedy_optimizer(player_team, opponent_team, max_turns=100)
            response_data = {
                'success': result.success,
                'totalDamage': result.total_damage,
                'turns': result.turns,
                'moveSequence': result.move_sequence
            }
        elif algorithm == 'dp':
            result = run_dp_optimizer(player_team, opponent_team, max_depth=50)
            response_data = {
                'success': result.success,
                'totalDamage': result.total_damage,
                'turns': result.turns,
                'moveSequence': result.move_sequence,
                'cacheHits': result.cache_hits,
                'cacheMisses': result.cache_misses,
                'cacheHitRate': result.get_cache_hit_rate(),
                'statesExplored': result.states_explored
            }
        else:  # dijkstra
            result = run_dijkstra_optimizer(player_team, opponent_team, max_states=500)
            response_data = {
                'success': result.success,
                'totalDamage': result.total_damage,
                'turns': result.turns,
                'moveSequence': result.move_sequence,
                'statesExplored': result.states_explored,
                'pathCost': result.path_cost
            }

        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'algorithm': algorithm,
                'result': response_data
            })
        }

    except json.JSONDecodeError:
        return error_response('Invalid JSON in request body', 400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(f'Internal server error: {str(e)}', 500)


def error_response(message: str, status_code: int) -> Dict[str, Any]:
    """Helper function to return error responses."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': False,
            'error': message
        })
    }


# For local testing
if __name__ == '__main__':
    from models.pokemon import create_pikachu, create_charizard

    # Test with actual Pokemon objects
    pikachu = create_pikachu(level=50)
    charizard = create_charizard(level=50)

    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'playerTeam': [pikachu.to_dict()],
            'opponentTeam': [charizard.to_dict()],
            'algorithm': 'greedy'
        })
    }

    print("Testing Battle Optimizer locally...")
    print("=" * 60)
    response = handler(test_event, None)
    print('Status Code:', response['statusCode'])
    print('Body:', json.dumps(json.loads(response['body']), indent=2))
