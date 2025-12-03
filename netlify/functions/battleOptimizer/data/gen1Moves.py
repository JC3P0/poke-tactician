"""
Gen 1 Move Database

Comprehensive database of Pokemon Gen 1 moves with accurate stats.
Used for converting MongoDB move names to Move objects.

Source: Bulbapedia Gen 1 move data
Author: Josh C.
Date: December 2025
"""

from models.move import Move

# Gen 1 Move Database
# Format: "move-name": (type, power, accuracy, pp)
GEN1_MOVES_DATA = {
    # Normal type moves
    "pound": ("Normal", 40, 100, 35),
    "karate-chop": ("Normal", 50, 100, 25),
    "double-slap": ("Normal", 15, 85, 10),
    "comet-punch": ("Normal", 18, 85, 15),
    "mega-punch": ("Normal", 80, 85, 20),
    "pay-day": ("Normal", 40, 100, 20),
    "scratch": ("Normal", 40, 100, 35),
    "vice-grip": ("Normal", 55, 100, 30),
    "guillotine": ("Normal", 0, 30, 5),  # OHKO
    "razor-wind": ("Normal", 80, 75, 10),
    "swords-dance": ("Normal", 0, 100, 30),
    "cut": ("Normal", 50, 95, 30),
    "gust": ("Normal", 40, 100, 35),
    "wing-attack": ("Flying", 35, 100, 35),
    "whirlwind": ("Normal", 0, 85, 20),
    "fly": ("Flying", 70, 95, 15),
    "bind": ("Normal", 15, 75, 20),
    "slam": ("Normal", 80, 75, 20),
    "vine-whip": ("Grass", 35, 100, 10),
    "stomp": ("Normal", 65, 100, 20),
    "double-kick": ("Fighting", 30, 100, 30),
    "mega-kick": ("Normal", 120, 75, 5),
    "jump-kick": ("Fighting", 70, 95, 25),
    "rolling-kick": ("Fighting", 60, 85, 15),
    "sand-attack": ("Normal", 0, 100, 15),
    "headbutt": ("Normal", 70, 100, 15),
    "horn-attack": ("Normal", 65, 100, 25),
    "fury-attack": ("Normal", 15, 85, 20),
    "horn-drill": ("Normal", 0, 30, 5),  # OHKO
    "tackle": ("Normal", 35, 95, 35),
    "body-slam": ("Normal", 85, 100, 15),
    "wrap": ("Normal", 15, 85, 20),
    "take-down": ("Normal", 90, 85, 20),
    "thrash": ("Normal", 90, 100, 20),
    "double-edge": ("Normal", 100, 100, 15),
    "tail-whip": ("Normal", 0, 100, 30),
    "poison-sting": ("Poison", 15, 100, 35),
    "twineedle": ("Bug", 25, 100, 20),
    "pin-missile": ("Bug", 14, 85, 20),
    "leer": ("Normal", 0, 100, 30),
    "bite": ("Normal", 60, 100, 25),
    "growl": ("Normal", 0, 100, 40),
    "roar": ("Normal", 0, 100, 20),
    "sing": ("Normal", 0, 55, 15),
    "supersonic": ("Normal", 0, 55, 20),
    "sonic-boom": ("Normal", 20, 90, 20),  # Fixed damage
    "disable": ("Normal", 0, 55, 20),
    "acid": ("Poison", 40, 100, 30),
    "ember": ("Fire", 40, 100, 25),
    "flamethrower": ("Fire", 95, 100, 15),
    "mist": ("Ice", 0, 100, 30),
    "water-gun": ("Water", 40, 100, 25),
    "hydro-pump": ("Water", 120, 80, 5),
    "surf": ("Water", 95, 100, 15),
    "ice-beam": ("Ice", 95, 100, 10),
    "blizzard": ("Ice", 120, 90, 5),
    "psybeam": ("Psychic", 65, 100, 20),
    "bubble-beam": ("Water", 65, 100, 20),
    "aurora-beam": ("Ice", 65, 100, 20),
    "hyper-beam": ("Normal", 150, 90, 5),
    "peck": ("Flying", 35, 100, 35),
    "drill-peck": ("Flying", 80, 100, 20),
    "submission": ("Fighting", 80, 80, 25),
    "low-kick": ("Fighting", 50, 90, 20),
    "counter": ("Fighting", 0, 100, 20),
    "seismic-toss": ("Fighting", 0, 100, 20),  # Level-based damage
    "strength": ("Normal", 80, 100, 15),
    "absorb": ("Grass", 20, 100, 20),
    "mega-drain": ("Grass", 40, 100, 10),
    "leech-seed": ("Grass", 0, 90, 10),
    "growth": ("Normal", 0, 100, 40),
    "razor-leaf": ("Grass", 55, 95, 25),
    "solar-beam": ("Grass", 120, 100, 10),
    "poison-powder": ("Poison", 0, 75, 35),
    "stun-spore": ("Grass", 0, 75, 30),
    "sleep-powder": ("Grass", 0, 75, 15),
    "petal-dance": ("Grass", 70, 100, 20),
    "string-shot": ("Bug", 0, 95, 40),
    "dragon-rage": ("Dragon", 40, 100, 10),  # Fixed damage
    "fire-spin": ("Fire", 15, 70, 15),
    "thunder-shock": ("Electric", 40, 100, 30),
    "thunderbolt": ("Electric", 95, 100, 15),
    "thunder-wave": ("Electric", 0, 100, 20),
    "thunder": ("Electric", 120, 70, 10),
    "rock-throw": ("Rock", 50, 65, 15),
    "earthquake": ("Ground", 100, 100, 10),
    "fissure": ("Ground", 0, 30, 5),  # OHKO
    "dig": ("Ground", 100, 100, 10),
    "toxic": ("Poison", 0, 85, 10),
    "confusion": ("Psychic", 50, 100, 25),
    "psychic": ("Psychic", 90, 100, 10),
    "hypnosis": ("Psychic", 0, 60, 20),
    "meditate": ("Psychic", 0, 100, 40),
    "agility": ("Psychic", 0, 100, 30),
    "quick-attack": ("Normal", 40, 100, 30),
    "rage": ("Normal", 20, 100, 20),
    "teleport": ("Psychic", 0, 100, 20),
    "night-shade": ("Ghost", 0, 100, 15),  # Level-based damage
    "mimic": ("Normal", 0, 100, 10),
    "screech": ("Normal", 0, 85, 40),
    "double-team": ("Normal", 0, 100, 15),
    "recover": ("Normal", 0, 100, 20),
    "harden": ("Normal", 0, 100, 30),
    "minimize": ("Normal", 0, 100, 20),
    "smokescreen": ("Normal", 0, 100, 20),
    "confuse-ray": ("Ghost", 0, 100, 10),
    "withdraw": ("Water", 0, 100, 40),
    "defense-curl": ("Normal", 0, 100, 40),
    "barrier": ("Psychic", 0, 100, 30),
    "light-screen": ("Psychic", 0, 100, 30),
    "haze": ("Ice", 0, 100, 30),
    "reflect": ("Psychic", 0, 100, 20),
    "focus-energy": ("Normal", 0, 100, 30),
    "bide": ("Normal", 0, 100, 10),
    "metronome": ("Normal", 0, 100, 10),
    "mirror-move": ("Flying", 0, 100, 20),
    "self-destruct": ("Normal", 130, 100, 5),
    "egg-bomb": ("Normal", 100, 75, 10),
    "lick": ("Ghost", 20, 100, 30),
    "smog": ("Poison", 20, 70, 20),
    "sludge": ("Poison", 65, 100, 20),
    "bone-club": ("Ground", 65, 85, 20),
    "fire-blast": ("Fire", 120, 85, 5),
    "waterfall": ("Water", 80, 100, 15),
    "clamp": ("Water", 35, 75, 10),
    "swift": ("Normal", 60, None, 20),  # Never misses
    "skull-bash": ("Normal", 100, 100, 15),
    "spike-cannon": ("Normal", 20, 100, 15),
    "constrict": ("Normal", 10, 100, 35),
    "amnesia": ("Psychic", 0, 100, 20),
    "kinesis": ("Psychic", 0, 80, 15),
    "soft-boiled": ("Normal", 0, 100, 10),
    "high-jump-kick": ("Fighting", 85, 90, 20),
    "glare": ("Normal", 0, 75, 30),
    "dream-eater": ("Psychic", 100, 100, 15),
    "poison-gas": ("Poison", 0, 55, 40),
    "barrage": ("Normal", 15, 85, 20),
    "leech-life": ("Bug", 20, 100, 15),
    "lovely-kiss": ("Normal", 0, 75, 10),
    "sky-attack": ("Flying", 140, 90, 5),
    "transform": ("Normal", 0, 100, 10),
    "bubble": ("Water", 20, 100, 30),
    "dizzy-punch": ("Normal", 70, 100, 10),
    "spore": ("Grass", 0, 100, 15),
    "flash": ("Normal", 0, 70, 20),
    "psywave": ("Psychic", 0, 80, 15),  # Variable damage
    "splash": ("Normal", 0, 100, 40),
    "acid-armor": ("Poison", 0, 100, 40),
    "crabhammer": ("Water", 90, 85, 10),
    "explosion": ("Normal", 170, 100, 5),
    "fury-swipes": ("Normal", 18, 80, 15),
    "bonemerang": ("Ground", 50, 90, 10),
    "rest": ("Psychic", 0, 100, 10),
    "rock-slide": ("Rock", 75, 90, 10),
    "hyper-fang": ("Normal", 80, 90, 15),
    "sharpen": ("Normal", 0, 100, 30),
    "conversion": ("Normal", 0, 100, 30),
    "tri-attack": ("Normal", 80, 100, 10),
    "super-fang": ("Normal", 0, 90, 10),  # Halves HP
    "slash": ("Normal", 70, 100, 20),
    "substitute": ("Normal", 0, 100, 10),
    "struggle": ("Normal", 50, 100, 1),
}


def get_move_by_name(move_name: str) -> Move:
    """
    Get a Move object by name from the Gen 1 move database.

    Args:
        move_name: Name of the move (lowercase, hyphenated format from MongoDB)

    Returns:
        Move object

    Raises:
        KeyError: If move not found in database
    """
    move_name_lower = move_name.lower()

    if move_name_lower not in GEN1_MOVES_DATA:
        raise KeyError(f"Move '{move_name}' not found in Gen 1 move database")

    move_type, power, accuracy, pp = GEN1_MOVES_DATA[move_name_lower]

    # Convert hyphenated name to title case (e.g., "thunder-shock" -> "Thunder Shock")
    display_name = " ".join(word.capitalize() for word in move_name.split("-"))

    return Move(
        name=display_name,
        move_type=move_type,
        power=power,
        accuracy=accuracy,
        pp=pp
    )


def get_random_moves_for_pokemon(pokemon_moves: list, count: int = 4) -> list:
    """
    Get a set of damaging moves for a Pokemon from its available moves.

    Prioritizes high-power damaging moves over status moves.

    Args:
        pokemon_moves: List of move names available to the Pokemon
        count: Number of moves to return (default 4)

    Returns:
        List of Move objects
    """
    available_moves = []

    for move_name in pokemon_moves:
        try:
            move = get_move_by_name(move_name)
            available_moves.append(move)
        except KeyError:
            # Skip unknown moves
            continue

    if not available_moves:
        # Fallback: Tackle
        return [Move("Tackle", "Normal", 35, 95, 35)]

    # Sort by power (prioritize damaging moves)
    damaging_moves = [m for m in available_moves if m.power > 0]
    status_moves = [m for m in available_moves if m.power == 0]

    # Sort damaging moves by power (descending)
    damaging_moves.sort(key=lambda m: m.power, reverse=True)

    # Take top damaging moves, fill with status if needed
    selected = damaging_moves[:count]
    if len(selected) < count:
        selected.extend(status_moves[:count - len(selected)])

    return selected[:count]
