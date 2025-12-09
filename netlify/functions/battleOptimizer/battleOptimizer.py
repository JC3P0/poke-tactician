"""
Pokemon Battle Optimizer - Netlify Serverless Function
CS_311 Extra Credit Project

This serverless function implements a Pokemon Gen 1 battle optimizer using
data structures and algorithms from CS_311 assignments.

Data Structures Used:
- Graph (Assignment 8 & 9): Battle state space representation + Dijkstra
- Hash Table (Assignment 7): Memoization cache for DP
- Heap (Assignment 6): Priority queue for Greedy move selection

Architecture: Uses Facade pattern (BattleOptimizerService) to hide complexity

Author: Josh C.
Date: December 2025
"""

import json
import sys
import os
import traceback
from typing import Dict, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import with error handling
try:
    from services.battleOptimizerService import BattleOptimizerService
    IMPORT_SUCCESS = True
    IMPORT_ERROR = None
except Exception as e:
    IMPORT_SUCCESS = False
    IMPORT_ERROR = f"Failed to import BattleOptimizerService: {str(e)}\n{traceback.format_exc()}"
    print(f"[CRITICAL] Import error: {IMPORT_ERROR}")


def handler(event, context):
    """
    AWS Lambda function handler (works with Lambda Function URLs).

    Expected POST body:
    {
        "playerTeam": [
            {
                "id": 25,
                "name": "pikachu",
                "types": ["electric"],
                "base_stats": {"hp": 35, "attack": 55, "defense": 40, "special": 50, "speed": 90},
                "moves": ["thunderbolt", "thunder-wave", "quick-attack", "thunder"]
            }
        ],
        "opponentTeam": [...] OR "bossTrainer": "blue" | "giovanni" | "lance",
        "algorithm": "greedy" | "dp" | "dijkstra" (default: "dijkstra"),
        "playerLevel": 50 (optional)
    }

    Returns:
    {
        "success": true,
        "result": {
            "success": true,
            "totalDamage": 500,
            "turns": 5,
            "moveSequence": ["Thunderbolt", "Thunder", ...],
            "algorithm": "dijkstra",
            "opponent": "Champion Blue",
            ...
        }
    }
    """

    # Check if imports succeeded
    if not IMPORT_SUCCESS:
        print(f"[ERROR] Handler called but imports failed: {IMPORT_ERROR}")
        return error_response(f'Import error: {IMPORT_ERROR}', 500)

    # Get HTTP method (Lambda Function URL format)
    http_method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    # Fallback to API Gateway format
    if not http_method or http_method == 'GET':
        http_method = event.get('httpMethod', 'GET')

    # Handle CORS preflight
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                
            },
            'body': ''
        }

    # Handle GET request for boss trainer list
    if http_method == 'GET':
        try:
            boss_trainers = BattleOptimizerService.get_boss_trainers()
            return success_response({"bossTrainers": boss_trainers})
        except Exception as e:
            return error_response(f'Error getting boss trainers: {str(e)}', 500)

    # Handle POST request for battle optimization
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))

        player_team_data = body.get('playerTeam', [])
        opponent_team_data = body.get('opponentTeam')
        boss_trainer_id = body.get('bossTrainer')
        algorithm = body.get('algorithm', 'dijkstra').lower()
        player_level = body.get('playerLevel', 50)

        # Validate player team
        if not player_team_data:
            return error_response('Missing player team data', 400)

        # Validate opponent
        if not opponent_team_data and not boss_trainer_id:
            return error_response('Must provide either opponentTeam or bossTrainer', 400)

        # Use the facade service to optimize the battle!
        result = BattleOptimizerService.optimize_battle(
            player_team_data=player_team_data,
            opponent_team_data=opponent_team_data,
            boss_trainer_id=boss_trainer_id,
            algorithm=algorithm,
            player_level=player_level
        )

        return success_response(result)

    except json.JSONDecodeError:
        return error_response('Invalid JSON in request body', 400)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(f'Internal server error: {str(e)}', 500)


def success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to return success responses."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'success': True,
            **data
        })
    }


def error_response(message: str, status_code: int) -> Dict[str, Any]:
    """Helper function to return error responses."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'success': False,
            'error': message
        })
    }


# For local testing
if __name__ == '__main__':
    # Simulate MongoDB Pokemon data format
    pikachu_data = {
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

    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'playerTeam': [pikachu_data],
            'bossTrainer': 'blue',  # Fight Champion Blue!
            'algorithm': 'greedy',
            'playerLevel': 65  # Same level as Blue's ace
        })
    }

    print("Testing Battle Optimizer with MongoDB format...")
    print("=" * 60)
    print("Player: Pikachu (Lv. 65)")
    print("Opponent: Champion Blue")
    print("Algorithm: Greedy")
    print("=" * 60)

    response = handler(test_event, None)
    print('\nStatus Code:', response['statusCode'])
    print('\nResponse:')
    print(json.dumps(json.loads(response['body']), indent=2))
