const mongoose = require('mongoose');

// Cache database connection across warm starts
let cachedDb = null;

async function connectToDatabase() {
  if (cachedDb && mongoose.connection.readyState === 1) {
    console.log('Using cached database connection');
    return cachedDb;
  }

  console.log('Establishing new database connection');
  await mongoose.connect(process.env.DATABASE_URL);
  cachedDb = mongoose.connection.db;
  return cachedDb;
}

/**
 * Netlify Function: Get Gen 1 Pokemon (IDs 1-151)
 *
 * Transforms modern Pokemon data to Gen 1 format:
 * - Merges Sp.Attack + Sp.Defense → Special stat
 * - Filters for Gen 1 Pokemon only (IDs 1-151)
 * - Returns Gen 1-accurate base stats
 *
 * Query params:
 *   - id: Pokemon ID (1-151)
 *   - page: Page number for pagination (default 1)
 *   - limit: Items per page (default 20)
 */
exports.handler = async (event, context) => {
  const { id, page = 1, limit = 20 } = event.queryStringParameters || {};

  try {
    // Establish database connection
    const db = await connectToDatabase();
    const pokemonCollection = db.collection('pokemons');

    // Single Pokemon query by ID
    if (id) {
      const pokemonId = parseInt(id);

      // Validate Gen 1 range (1-151)
      if (pokemonId < 1 || pokemonId > 151) {
        return {
          statusCode: 400,
          body: JSON.stringify({
            message: 'Invalid Pokemon ID. Gen 1 Pokemon range is 1-151.'
          }),
        };
      }

      const pokemon = await pokemonCollection.findOne({ id: pokemonId });

      if (!pokemon) {
        return {
          statusCode: 404,
          body: JSON.stringify({ message: 'Pokemon not found' }),
        };
      }

      // Transform to Gen 1 format
      const gen1Pokemon = transformToGen1(pokemon);

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*', // Enable CORS
        },
        body: JSON.stringify(gen1Pokemon),
      };
    }

    // Paginated list of all Gen 1 Pokemon
    const skip = (parseInt(page) - 1) * parseInt(limit);

    const pokemon = await pokemonCollection
      .find({ id: { $gte: 1, $lte: 151 } }) // Gen 1 only
      .sort({ id: 1 })
      .skip(skip)
      .limit(parseInt(limit))
      .toArray();

    const total = await pokemonCollection.countDocuments({
      id: { $gte: 1, $lte: 151 }
    });

    // Transform all Pokemon to Gen 1 format
    const gen1Pokemon = pokemon.map(transformToGen1);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        pokemon: gen1Pokemon,
        total,
        page: parseInt(page),
        pages: Math.ceil(total / parseInt(limit)),
      }),
    };

  } catch (err) {
    console.error('Error fetching Gen 1 Pokemon:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: err.message }),
    };
  }
};

/**
 * Transform modern Pokemon data to Gen 1 format
 *
 * Key transformations:
 * - Merge Sp.Attack (index 3) + Sp.Defense (index 4) → Special stat
 * - Extract only Gen 1 relevant data
 * - Calculate average for unified Special stat
 */
function transformToGen1(pokemon) {
  // Pokemon stats array from PokeAPI:
  // [0] = HP, [1] = Attack, [2] = Defense
  // [3] = Sp.Attack, [4] = Sp.Defense, [5] = Speed

  const stats = pokemon.stats || [];

  // Merge Sp.Attack and Sp.Defense into unified Special stat
  const spAttack = stats.find(s => s.name === 'special-attack')?.base_stat || 0;
  const spDefense = stats.find(s => s.name === 'special-defense')?.base_stat || 0;
  const special = Math.floor((spAttack + spDefense) / 2);

  return {
    id: pokemon.id,
    name: pokemon.name,
    types: pokemon.types?.map(t => t.name) || [],
    base_stats: {
      hp: stats.find(s => s.name === 'hp')?.base_stat || 0,
      attack: stats.find(s => s.name === 'attack')?.base_stat || 0,
      defense: stats.find(s => s.name === 'defense')?.base_stat || 0,
      special: special, // Unified Gen 1 Special stat!
      speed: stats.find(s => s.name === 'speed')?.base_stat || 0,
    },
    sprites: {
      front_default: pokemon.sprites?.front_default,
      back_default: pokemon.sprites?.back_default,
      front_shiny: pokemon.sprites?.front_shiny,
      back_shiny: pokemon.sprites?.back_shiny,
    },
    // Include move names (we'll filter to Gen 1 moves later)
    moves: pokemon.moves?.map(m => m.name) || [],
    base_experience: pokemon.base_experience,
    height: pokemon.height,
    weight: pokemon.weight,
  };
}
