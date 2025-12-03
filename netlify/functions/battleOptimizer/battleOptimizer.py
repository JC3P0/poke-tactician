"""
Pokemon Battle Optimizer - Netlify Serverless Function
CS_311 Extra Credit Project

This serverless function implements a Pokemon Gen 1 battle optimizer using
data structures and algorithms from CS_311 assignments.

Data Structures Used:
- Graph (Assignment 8): Battle state space representation
- Hash Table (Assignment 7): Memoization cache
- Heap (Assignment 6): Priority queue for move selection
- Dijkstra's Algorithm (Assignment 9): Optimal path finding

Author: Josh C.
Date: December 2025
"""

import json
from typing import Dict, List, Any

# Import our data structures (to be implemented)
# from dataStructures.graph import Graph
# from dataStructures.hashtable import HashTable
# from dataStructures.heap import Heap
# from algorithms.dijkstra import findOptimalPath
# from algorithms.greedy import GreedyOptimizer
# from models.battleState import BattleState
# from models.pokemon import Pokemon


def handler(event, context):
    """
    Netlify serverless function handler.

    Expected POST body:
    {
        "yourTeam": [Pokemon objects],
        "opponentTeam": [Pokemon objects],
        "algorithm": "dijkstra" | "greedy" | "bfs"
    }

    Returns:
    {
        "success": true,
        "strategy": [list of moves],
        "totalDamage": int,
        "totalTurns": int,
        "algorithm": string
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
        your_team = body.get('yourTeam', [])
        opponent_team = body.get('opponentTeam', [])
        algorithm = body.get('algorithm', 'dijkstra')

        # Validate input
        if not your_team or not opponent_team:
            return error_response('Missing team data', 400)

        # TODO: Implement optimization algorithms
        # For now, return a placeholder response
        result = {
            'success': True,
            'message': 'Optimizer under construction! Python structure ready.',
            'algorithm': algorithm,
            'yourTeam': your_team,
            'opponentTeam': opponent_team,
            'strategy': [],
            'totalDamage': 0,
            'totalTurns': 0
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }

    except json.JSONDecodeError:
        return error_response('Invalid JSON in request body', 400)
    except Exception as e:
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
    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'yourTeam': [
                {'id': 25, 'name': 'Pikachu', 'level': 100}
            ],
            'opponentTeam': [
                {'id': 19, 'name': 'Rattata', 'level': 5}
            ],
            'algorithm': 'dijkstra'
        })
    }

    response = handler(test_event, None)
    print('Status Code:', response['statusCode'])
    print('Body:', json.loads(response['body']))
