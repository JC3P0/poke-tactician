/**
 * Gen 1 Move Database
 *
 * Comprehensive database of Pokemon Gen 1 moves with accurate stats.
 * Used for displaying move details in the UI.
 *
 * Format: "move-name": { type, power, accuracy, pp }
 *
 * Source: Bulbapedia Gen 1 move data
 * Author: Josh C.
 * Date: December 2025
 */

export const GEN1_MOVES_DATA = {
  // Normal type moves
  "pound": { type: "Normal", power: 40, accuracy: 100, pp: 35 },
  "karate-chop": { type: "Normal", power: 50, accuracy: 100, pp: 25 },
  "double-slap": { type: "Normal", power: 15, accuracy: 85, pp: 10 },
  "comet-punch": { type: "Normal", power: 18, accuracy: 85, pp: 15 },
  "mega-punch": { type: "Normal", power: 80, accuracy: 85, pp: 20 },
  "pay-day": { type: "Normal", power: 40, accuracy: 100, pp: 20 },
  "scratch": { type: "Normal", power: 40, accuracy: 100, pp: 35 },
  "vice-grip": { type: "Normal", power: 55, accuracy: 100, pp: 30 },
  "guillotine": { type: "Normal", power: 0, accuracy: 30, pp: 5 },
  "razor-wind": { type: "Normal", power: 80, accuracy: 75, pp: 10 },
  "swords-dance": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "cut": { type: "Normal", power: 50, accuracy: 95, pp: 30 },
  "gust": { type: "Normal", power: 40, accuracy: 100, pp: 35 },
  "wing-attack": { type: "Flying", power: 35, accuracy: 100, pp: 35 },
  "whirlwind": { type: "Normal", power: 0, accuracy: 85, pp: 20 },
  "fly": { type: "Flying", power: 70, accuracy: 95, pp: 15 },
  "bind": { type: "Normal", power: 15, accuracy: 75, pp: 20 },
  "slam": { type: "Normal", power: 80, accuracy: 75, pp: 20 },
  "vine-whip": { type: "Grass", power: 35, accuracy: 100, pp: 10 },
  "stomp": { type: "Normal", power: 65, accuracy: 100, pp: 20 },
  "double-kick": { type: "Fighting", power: 30, accuracy: 100, pp: 30 },
  "mega-kick": { type: "Normal", power: 120, accuracy: 75, pp: 5 },
  "jump-kick": { type: "Fighting", power: 70, accuracy: 95, pp: 25 },
  "rolling-kick": { type: "Fighting", power: 60, accuracy: 85, pp: 15 },
  "sand-attack": { type: "Normal", power: 0, accuracy: 100, pp: 15 },
  "headbutt": { type: "Normal", power: 70, accuracy: 100, pp: 15 },
  "horn-attack": { type: "Normal", power: 65, accuracy: 100, pp: 25 },
  "fury-attack": { type: "Normal", power: 15, accuracy: 85, pp: 20 },
  "horn-drill": { type: "Normal", power: 0, accuracy: 30, pp: 5 },
  "tackle": { type: "Normal", power: 35, accuracy: 95, pp: 35 },
  "body-slam": { type: "Normal", power: 85, accuracy: 100, pp: 15 },
  "wrap": { type: "Normal", power: 15, accuracy: 85, pp: 20 },
  "take-down": { type: "Normal", power: 90, accuracy: 85, pp: 20 },
  "thrash": { type: "Normal", power: 90, accuracy: 100, pp: 20 },
  "double-edge": { type: "Normal", power: 100, accuracy: 100, pp: 15 },
  "tail-whip": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "poison-sting": { type: "Poison", power: 15, accuracy: 100, pp: 35 },
  "twineedle": { type: "Bug", power: 25, accuracy: 100, pp: 20 },
  "pin-missile": { type: "Bug", power: 14, accuracy: 85, pp: 20 },
  "leer": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "bite": { type: "Normal", power: 60, accuracy: 100, pp: 25 },
  "growl": { type: "Normal", power: 0, accuracy: 100, pp: 40 },
  "roar": { type: "Normal", power: 0, accuracy: 100, pp: 20 },
  "sing": { type: "Normal", power: 0, accuracy: 55, pp: 15 },
  "supersonic": { type: "Normal", power: 0, accuracy: 55, pp: 20 },
  "sonic-boom": { type: "Normal", power: 20, accuracy: 90, pp: 20 },
  "disable": { type: "Normal", power: 0, accuracy: 55, pp: 20 },
  "acid": { type: "Poison", power: 40, accuracy: 100, pp: 30 },
  "ember": { type: "Fire", power: 40, accuracy: 100, pp: 25 },
  "flamethrower": { type: "Fire", power: 95, accuracy: 100, pp: 15 },
  "mist": { type: "Ice", power: 0, accuracy: 100, pp: 30 },
  "water-gun": { type: "Water", power: 40, accuracy: 100, pp: 25 },
  "hydro-pump": { type: "Water", power: 120, accuracy: 80, pp: 5 },
  "surf": { type: "Water", power: 95, accuracy: 100, pp: 15 },
  "ice-beam": { type: "Ice", power: 95, accuracy: 100, pp: 10 },
  "blizzard": { type: "Ice", power: 120, accuracy: 90, pp: 5 },
  "psybeam": { type: "Psychic", power: 65, accuracy: 100, pp: 20 },
  "bubble-beam": { type: "Water", power: 65, accuracy: 100, pp: 20 },
  "aurora-beam": { type: "Ice", power: 65, accuracy: 100, pp: 20 },
  "hyper-beam": { type: "Normal", power: 150, accuracy: 90, pp: 5 },
  "peck": { type: "Flying", power: 35, accuracy: 100, pp: 35 },
  "drill-peck": { type: "Flying", power: 80, accuracy: 100, pp: 20 },
  "submission": { type: "Fighting", power: 80, accuracy: 80, pp: 25 },
  "low-kick": { type: "Fighting", power: 50, accuracy: 90, pp: 20 },
  "counter": { type: "Fighting", power: 0, accuracy: 100, pp: 20 },
  "seismic-toss": { type: "Fighting", power: 0, accuracy: 100, pp: 20 },
  "strength": { type: "Normal", power: 80, accuracy: 100, pp: 15 },
  "absorb": { type: "Grass", power: 20, accuracy: 100, pp: 20 },
  "mega-drain": { type: "Grass", power: 40, accuracy: 100, pp: 10 },
  "leech-seed": { type: "Grass", power: 0, accuracy: 90, pp: 10 },
  "growth": { type: "Normal", power: 0, accuracy: 100, pp: 40 },
  "razor-leaf": { type: "Grass", power: 55, accuracy: 95, pp: 25 },
  "solar-beam": { type: "Grass", power: 120, accuracy: 100, pp: 10 },
  "poison-powder": { type: "Poison", power: 0, accuracy: 75, pp: 35 },
  "stun-spore": { type: "Grass", power: 0, accuracy: 75, pp: 30 },
  "sleep-powder": { type: "Grass", power: 0, accuracy: 75, pp: 15 },
  "petal-dance": { type: "Grass", power: 70, accuracy: 100, pp: 20 },
  "string-shot": { type: "Bug", power: 0, accuracy: 95, pp: 40 },
  "dragon-rage": { type: "Dragon", power: 40, accuracy: 100, pp: 10 },
  "fire-spin": { type: "Fire", power: 15, accuracy: 70, pp: 15 },
  "thunder-shock": { type: "Electric", power: 40, accuracy: 100, pp: 30 },
  "thunderbolt": { type: "Electric", power: 95, accuracy: 100, pp: 15 },
  "thunder-wave": { type: "Electric", power: 0, accuracy: 100, pp: 20 },
  "thunder": { type: "Electric", power: 120, accuracy: 70, pp: 10 },
  "rock-throw": { type: "Rock", power: 50, accuracy: 65, pp: 15 },
  "earthquake": { type: "Ground", power: 100, accuracy: 100, pp: 10 },
  "fissure": { type: "Ground", power: 0, accuracy: 30, pp: 5 },
  "dig": { type: "Ground", power: 100, accuracy: 100, pp: 10 },
  "toxic": { type: "Poison", power: 0, accuracy: 85, pp: 10 },
  "confusion": { type: "Psychic", power: 50, accuracy: 100, pp: 25 },
  "psychic": { type: "Psychic", power: 90, accuracy: 100, pp: 10 },
  "hypnosis": { type: "Psychic", power: 0, accuracy: 60, pp: 20 },
  "meditate": { type: "Psychic", power: 0, accuracy: 100, pp: 40 },
  "agility": { type: "Psychic", power: 0, accuracy: 100, pp: 30 },
  "quick-attack": { type: "Normal", power: 40, accuracy: 100, pp: 30 },
  "rage": { type: "Normal", power: 20, accuracy: 100, pp: 20 },
  "teleport": { type: "Psychic", power: 0, accuracy: 100, pp: 20 },
  "night-shade": { type: "Ghost", power: 0, accuracy: 100, pp: 15 },
  "mimic": { type: "Normal", power: 0, accuracy: 100, pp: 10 },
  "screech": { type: "Normal", power: 0, accuracy: 85, pp: 40 },
  "double-team": { type: "Normal", power: 0, accuracy: 100, pp: 15 },
  "recover": { type: "Normal", power: 0, accuracy: 100, pp: 20 },
  "harden": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "minimize": { type: "Normal", power: 0, accuracy: 100, pp: 20 },
  "smokescreen": { type: "Normal", power: 0, accuracy: 100, pp: 20 },
  "confuse-ray": { type: "Ghost", power: 0, accuracy: 100, pp: 10 },
  "withdraw": { type: "Water", power: 0, accuracy: 100, pp: 40 },
  "defense-curl": { type: "Normal", power: 0, accuracy: 100, pp: 40 },
  "barrier": { type: "Psychic", power: 0, accuracy: 100, pp: 30 },
  "light-screen": { type: "Psychic", power: 0, accuracy: 100, pp: 30 },
  "haze": { type: "Ice", power: 0, accuracy: 100, pp: 30 },
  "reflect": { type: "Psychic", power: 0, accuracy: 100, pp: 20 },
  "focus-energy": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "bide": { type: "Normal", power: 0, accuracy: 100, pp: 10 },
  "metronome": { type: "Normal", power: 0, accuracy: 100, pp: 10 },
  "mirror-move": { type: "Flying", power: 0, accuracy: 100, pp: 20 },
  "self-destruct": { type: "Normal", power: 130, accuracy: 100, pp: 5 },
  "egg-bomb": { type: "Normal", power: 100, accuracy: 75, pp: 10 },
  "lick": { type: "Ghost", power: 20, accuracy: 100, pp: 30 },
  "smog": { type: "Poison", power: 20, accuracy: 70, pp: 20 },
  "sludge": { type: "Poison", power: 65, accuracy: 100, pp: 20 },
  "bone-club": { type: "Ground", power: 65, accuracy: 85, pp: 20 },
  "fire-blast": { type: "Fire", power: 120, accuracy: 85, pp: 5 },
  "waterfall": { type: "Water", power: 80, accuracy: 100, pp: 15 },
  "clamp": { type: "Water", power: 35, accuracy: 75, pp: 10 },
  "swift": { type: "Normal", power: 60, accuracy: null, pp: 20 },
  "skull-bash": { type: "Normal", power: 100, accuracy: 100, pp: 15 },
  "spike-cannon": { type: "Normal", power: 20, accuracy: 100, pp: 15 },
  "constrict": { type: "Normal", power: 10, accuracy: 100, pp: 35 },
  "amnesia": { type: "Psychic", power: 0, accuracy: 100, pp: 20 },
  "kinesis": { type: "Psychic", power: 0, accuracy: 80, pp: 15 },
  "soft-boiled": { type: "Normal", power: 0, accuracy: 100, pp: 10 },
  "high-jump-kick": { type: "Fighting", power: 85, accuracy: 90, pp: 20 },
  "glare": { type: "Normal", power: 0, accuracy: 75, pp: 30 },
  "dream-eater": { type: "Psychic", power: 100, accuracy: 100, pp: 15 },
  "poison-gas": { type: "Poison", power: 0, accuracy: 55, pp: 40 },
  "barrage": { type: "Normal", power: 15, accuracy: 85, pp: 20 },
  "leech-life": { type: "Bug", power: 20, accuracy: 100, pp: 15 },
  "lovely-kiss": { type: "Normal", power: 0, accuracy: 75, pp: 10 },
  "sky-attack": { type: "Flying", power: 140, accuracy: 90, pp: 5 },
  "transform": { type: "Normal", power: 0, accuracy: 100, pp: 10 },
  "bubble": { type: "Water", power: 20, accuracy: 100, pp: 30 },
  "dizzy-punch": { type: "Normal", power: 70, accuracy: 100, pp: 10 },
  "spore": { type: "Grass", power: 0, accuracy: 100, pp: 15 },
  "flash": { type: "Normal", power: 0, accuracy: 70, pp: 20 },
  "psywave": { type: "Psychic", power: 0, accuracy: 80, pp: 15 },
  "splash": { type: "Normal", power: 0, accuracy: 100, pp: 40 },
  "acid-armor": { type: "Poison", power: 0, accuracy: 100, pp: 40 },
  "crabhammer": { type: "Water", power: 90, accuracy: 85, pp: 10 },
  "explosion": { type: "Normal", power: 170, accuracy: 100, pp: 5 },
  "fury-swipes": { type: "Normal", power: 18, accuracy: 80, pp: 15 },
  "bonemerang": { type: "Ground", power: 50, accuracy: 90, pp: 10 },
  "rest": { type: "Psychic", power: 0, accuracy: 100, pp: 10 },
  "rock-slide": { type: "Rock", power: 75, accuracy: 90, pp: 10 },
  "hyper-fang": { type: "Normal", power: 80, accuracy: 90, pp: 15 },
  "sharpen": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "conversion": { type: "Normal", power: 0, accuracy: 100, pp: 30 },
  "tri-attack": { type: "Normal", power: 80, accuracy: 100, pp: 10 },
  "super-fang": { type: "Normal", power: 0, accuracy: 90, pp: 10 },
  "slash": { type: "Normal", power: 70, accuracy: 100, pp: 20 },
  "substitute": { type: "Normal", power: 0, accuracy: 100, pp: 10 },
  "struggle": { type: "Normal", power: 50, accuracy: 100, pp: 1 },
};

/**
 * Get move details by name
 * @param {string} moveName - Hyphenated move name (e.g., "thunder-shock")
 * @returns {object|null} Move data or null if not found
 */
export const getMoveData = (moveName) => {
  if (!moveName) return null;
  return GEN1_MOVES_DATA[moveName.toLowerCase()] || null;
};

/**
 * Format move display text
 * @param {string} moveName - Hyphenated move name
 * @returns {string} Formatted display text with power and PP
 */
export const formatMoveDisplay = (moveName) => {
  if (!moveName) return '';

  const moveData = getMoveData(moveName);
  const displayName = moveName
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');

  if (!moveData) {
    return displayName;
  }

  // For status moves (power = 0), only show PP
  if (moveData.power === 0) {
    return `${displayName} (Status, ${moveData.pp} PP)`;
  }

  // For damaging moves, show power and PP
  return `${displayName} (${moveData.power} power, ${moveData.pp} PP)`;
};
