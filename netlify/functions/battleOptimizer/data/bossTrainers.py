"""
Boss Trainer Data - Iconic Gen 1 Trainers

Contains pre-built teams for famous Pokemon Gen 1 trainers:
- Champion Blue (Gary)
- Giovanni (Viridian Gym Leader)
- Lance (Elite Four Champion before Blue)

All Pokemon use accurate Gen 1 base stats and movesets.

Author: Josh C.
Date: December 2025
CS_311 Extra Credit Project
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pokemon import Pokemon
from models.move import Move


def create_champion_blue() -> list:
    """
    Create Champion Blue's (Gary's) team from Pokemon Red/Blue.

    This is his final team if you chose Charmander as your starter.
    All Pokemon are level 61-65 (his highest levels in Gen 1).

    Returns:
        List of 6 Pokemon representing Blue's champion team
    """
    # Pidgeot (Level 61)
    pidgeot = Pokemon(
        name="Pidgeot",
        types=["Normal", "Flying"],
        level=61,
        base_stats={
            "HP": 83,
            "Attack": 80,
            "Defense": 75,
            "Speed": 91,
            "Special": 70
        },
        moves=[
            Move("Wing Attack", "Flying", 35, 100, 35),
            Move("Sky Attack", "Flying", 140, 90, 5),
            Move("Mirror Move", "Flying", 0, 100, 20),
            Move("Agility", "Psychic", 0, 100, 30)
        ]
    )

    # Alakazam (Level 59)
    alakazam = Pokemon(
        name="Alakazam",
        types=["Psychic"],
        level=59,
        base_stats={
            "HP": 55,
            "Attack": 50,
            "Defense": 45,
            "Speed": 120,
            "Special": 135
        },
        moves=[
            Move("Psychic", "Psychic", 90, 100, 10),
            Move("Psybeam", "Psychic", 65, 100, 20),
            Move("Recover", "Normal", 0, 100, 20),
            Move("Reflect", "Psychic", 0, 100, 20)
        ]
    )

    # Rhydon (Level 61)
    rhydon = Pokemon(
        name="Rhydon",
        types=["Ground", "Rock"],
        level=61,
        base_stats={
            "HP": 105,
            "Attack": 130,
            "Defense": 120,
            "Speed": 40,
            "Special": 45
        },
        moves=[
            Move("Earthquake", "Ground", 100, 100, 10),
            Move("Rock Slide", "Rock", 75, 90, 10),
            Move("Horn Drill", "Normal", 0, 30, 5),
            Move("Tail Whip", "Normal", 0, 100, 30)
        ]
    )

    # Gyarados (Level 61)
    gyarados = Pokemon(
        name="Gyarados",
        types=["Water", "Flying"],
        level=61,
        base_stats={
            "HP": 95,
            "Attack": 125,
            "Defense": 79,
            "Speed": 81,
            "Special": 100
        },
        moves=[
            Move("Hydro Pump", "Water", 120, 80, 5),
            Move("Surf", "Water", 95, 100, 15),
            Move("Dragon Rage", "Dragon", 40, 100, 10),
            Move("Hyper Beam", "Normal", 150, 90, 5)
        ]
    )

    # Arcanine (Level 63)
    arcanine = Pokemon(
        name="Arcanine",
        types=["Fire"],
        level=63,
        base_stats={
            "HP": 90,
            "Attack": 110,
            "Defense": 80,
            "Speed": 95,
            "Special": 80
        },
        moves=[
            Move("Flamethrower", "Fire", 95, 100, 15),
            Move("Fire Blast", "Fire", 120, 85, 5),
            Move("Take Down", "Normal", 90, 85, 20),
            Move("Reflect", "Psychic", 0, 100, 20)
        ]
    )

    # Blastoise (Level 65) - His starter (if you chose Charmander)
    blastoise = Pokemon(
        name="Blastoise",
        types=["Water"],
        level=65,
        base_stats={
            "HP": 79,
            "Attack": 83,
            "Defense": 100,
            "Speed": 78,
            "Special": 85
        },
        moves=[
            Move("Surf", "Water", 95, 100, 15),
            Move("Ice Beam", "Ice", 95, 100, 10),
            Move("Blizzard", "Ice", 120, 90, 5),
            Move("Withdraw", "Water", 0, 100, 40)
        ]
    )

    return [pidgeot, alakazam, rhydon, gyarados, arcanine, blastoise]


def create_giovanni() -> list:
    """
    Create Giovanni's team from Viridian Gym (8th Gym).

    Ground-type specialist and Team Rocket leader.
    All Pokemon are level 42-55 (his highest levels).

    Returns:
        List of 5 Pokemon representing Giovanni's gym team
    """
    # Rhyhorn (Level 45)
    rhyhorn = Pokemon(
        name="Rhyhorn",
        types=["Ground", "Rock"],
        level=45,
        base_stats={
            "HP": 80,
            "Attack": 85,
            "Defense": 95,
            "Speed": 25,
            "Special": 30
        },
        moves=[
            Move("Horn Attack", "Normal", 65, 100, 25),
            Move("Stomp", "Normal", 65, 100, 20),
            Move("Tail Whip", "Normal", 0, 100, 30),
            Move("Fury Attack", "Normal", 15, 85, 20)
        ]
    )

    # Dugtrio (Level 50)
    dugtrio = Pokemon(
        name="Dugtrio",
        types=["Ground"],
        level=50,
        base_stats={
            "HP": 35,
            "Attack": 80,
            "Defense": 50,
            "Speed": 120,
            "Special": 70
        },
        moves=[
            Move("Earthquake", "Ground", 100, 100, 10),
            Move("Dig", "Ground", 100, 100, 10),
            Move("Slash", "Normal", 70, 100, 20),
            Move("Sand Attack", "Normal", 0, 100, 15)
        ]
    )

    # Nidoqueen (Level 53)
    nidoqueen = Pokemon(
        name="Nidoqueen",
        types=["Poison", "Ground"],
        level=53,
        base_stats={
            "HP": 90,
            "Attack": 82,
            "Defense": 87,
            "Speed": 76,
            "Special": 75
        },
        moves=[
            Move("Earthquake", "Ground", 100, 100, 10),
            Move("Thunder", "Electric", 120, 70, 10),
            Move("Body Slam", "Normal", 85, 100, 15),
            Move("Poison Sting", "Poison", 15, 100, 35)
        ]
    )

    # Nidoking (Level 53)
    nidoking = Pokemon(
        name="Nidoking",
        types=["Poison", "Ground"],
        level=53,
        base_stats={
            "HP": 81,
            "Attack": 92,
            "Defense": 77,
            "Speed": 85,
            "Special": 75
        },
        moves=[
            Move("Earthquake", "Ground", 100, 100, 10),
            Move("Thunderbolt", "Electric", 95, 100, 15),
            Move("Thrash", "Normal", 90, 100, 20),
            Move("Horn Attack", "Normal", 65, 100, 25)
        ]
    )

    # Rhydon (Level 55) - His ace
    rhydon = Pokemon(
        name="Rhydon",
        types=["Ground", "Rock"],
        level=55,
        base_stats={
            "HP": 105,
            "Attack": 130,
            "Defense": 120,
            "Speed": 40,
            "Special": 45
        },
        moves=[
            Move("Earthquake", "Ground", 100, 100, 10),
            Move("Rock Slide", "Rock", 75, 90, 10),
            Move("Horn Drill", "Normal", 0, 30, 5),
            Move("Fury Attack", "Normal", 15, 85, 20)
        ]
    )

    return [rhyhorn, dugtrio, nidoqueen, nidoking, rhydon]


def create_lance() -> list:
    """
    Create Lance's team from Elite Four.

    Dragon-type specialist (though only Dragonite is actually Dragon-type in Gen 1!)
    All Pokemon are level 56-62.

    Returns:
        List of 5 Pokemon representing Lance's team
    """
    # Gyarados (Level 58)
    gyarados = Pokemon(
        name="Gyarados",
        types=["Water", "Flying"],
        level=58,
        base_stats={
            "HP": 95,
            "Attack": 125,
            "Defense": 79,
            "Speed": 81,
            "Special": 100
        },
        moves=[
            Move("Hydro Pump", "Water", 120, 80, 5),
            Move("Dragon Rage", "Dragon", 40, 100, 10),
            Move("Hyper Beam", "Normal", 150, 90, 5),
            Move("Leer", "Normal", 0, 100, 30)
        ]
    )

    # Dragonair (Level 56)
    dragonair = Pokemon(
        name="Dragonair",
        types=["Dragon"],
        level=56,
        base_stats={
            "HP": 61,
            "Attack": 84,
            "Defense": 65,
            "Speed": 70,
            "Special": 70
        },
        moves=[
            Move("Slam", "Normal", 80, 75, 20),
            Move("Agility", "Psychic", 0, 100, 30),
            Move("Hyper Beam", "Normal", 150, 90, 5),
            Move("Wrap", "Normal", 15, 85, 20)
        ]
    )

    # Dragonair #2 (Level 56)
    dragonair2 = Pokemon(
        name="Dragonair",
        types=["Dragon"],
        level=56,
        base_stats={
            "HP": 61,
            "Attack": 84,
            "Defense": 65,
            "Speed": 70,
            "Special": 70
        },
        moves=[
            Move("Thunder Wave", "Electric", 0, 100, 20),
            Move("Slam", "Normal", 80, 75, 20),
            Move("Dragon Rage", "Dragon", 40, 100, 10),
            Move("Hyper Beam", "Normal", 150, 90, 5)
        ]
    )

    # Aerodactyl (Level 60)
    aerodactyl = Pokemon(
        name="Aerodactyl",
        types=["Rock", "Flying"],
        level=60,
        base_stats={
            "HP": 80,
            "Attack": 105,
            "Defense": 65,
            "Speed": 130,
            "Special": 60
        },
        moves=[
            Move("Wing Attack", "Flying", 35, 100, 35),
            Move("Agility", "Psychic", 0, 100, 30),
            Move("Supersonic", "Normal", 0, 55, 20),
            Move("Take Down", "Normal", 90, 85, 20)
        ]
    )

    # Dragonite (Level 62) - His ace
    dragonite = Pokemon(
        name="Dragonite",
        types=["Dragon", "Flying"],
        level=62,
        base_stats={
            "HP": 91,
            "Attack": 134,
            "Defense": 95,
            "Speed": 80,
            "Special": 100
        },
        moves=[
            Move("Blizzard", "Ice", 120, 90, 5),
            Move("Fire Blast", "Fire", 120, 85, 5),
            Move("Thunder", "Electric", 120, 70, 10),
            Move("Hyper Beam", "Normal", 150, 90, 5)
        ]
    )

    return [gyarados, dragonair, dragonair2, aerodactyl, dragonite]


# Dictionary for easy access
BOSS_TRAINERS = {
    "blue": {
        "name": "Champion Blue",
        "title": "Pokemon Champion",
        "team": create_champion_blue,
        "description": "Your rival who became the Pokemon Champion! Can you defeat his balanced team?"
    },
    "giovanni": {
        "name": "Giovanni",
        "title": "Team Rocket Boss & Viridian Gym Leader",
        "team": create_giovanni,
        "description": "The Ground-type master and leader of Team Rocket. His powerful Pokemon are no joke!"
    },
    "lance": {
        "name": "Lance",
        "title": "Elite Four Dragon Master",
        "team": create_lance,
        "description": "Master of Dragon Pokemon! His Dragonite knows every elemental attack."
    }
}


def get_boss_trainer(trainer_id: str) -> dict:
    """
    Get a boss trainer's data.

    Args:
        trainer_id: ID of the trainer ("blue", "giovanni", "lance")

    Returns:
        Dictionary with trainer info and team
    """
    if trainer_id not in BOSS_TRAINERS:
        raise ValueError(f"Unknown trainer: {trainer_id}")

    trainer_data = BOSS_TRAINERS[trainer_id].copy()
    trainer_data["team"] = trainer_data["team"]()  # Call function to get team
    return trainer_data
