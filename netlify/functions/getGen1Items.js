const mongoose = require('mongoose');

// Connect to MongoDB (uses DATABASE_URL environment variable from Netlify)
mongoose.connect(process.env.DATABASE_URL);

/**
 * Gen 1 Battle-Usable Items
 *
 * These items can be used during battles in Pokemon Red/Blue.
 * Source: Bulbapedia - "List of items by index number (Generation I)"
 * https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_I)
 */
const GEN1_BATTLE_ITEMS = [
  // Healing Items
  'potion',
  'super-potion',
  'hyper-potion',
  'max-potion',
  'full-restore',

  // Revival Items
  'revive',
  'max-revive',

  // Status Healers
  'antidote',       // Cures poison
  'burn-heal',      // Cures burn
  'ice-heal',       // Cures freeze
  'awakening',      // Cures sleep
  'paralyze-heal',  // Cures paralysis
  'full-heal',      // Cures all status conditions

  // Stat Boosters (temporary, in-battle)
  'x-attack',       // Raises Attack
  'x-defend',       // Raises Defense
  'x-speed',        // Raises Speed
  'x-special',      // Raises Special
  'dire-hit',       // Increases critical hit ratio
  'guard-spec',     // Prevents stat reduction
];

/**
 * Netlify Function: Get Gen 1 Battle Items
 *
 * Filters items to only those usable in Gen 1 battles.
 * Excludes held items (don't exist in Gen 1), TMs, key items, etc.
 *
 * Query params:
 *   - id: Item ID
 *   - name: Item name
 *   - category: Filter by category (healing, revival, status, stat-boost)
 */
exports.handler = async (event, context) => {
  const { id, name, category } = event.queryStringParameters || {};

  try {
    const db = mongoose.connection.db;
    const itemsCollection = db.collection('items');

    // Single item query by ID or name
    if (id || name) {
      let query = {};

      if (id) {
        query.id = parseInt(id);
      } else if (name) {
        query.name = name.toLowerCase().replace(/\s+/g, '-');
      }

      const item = await itemsCollection.findOne(query);

      if (!item) {
        return {
          statusCode: 404,
          body: JSON.stringify({ message: 'Item not found' }),
        };
      }

      // Check if item is Gen 1 battle-usable
      if (!GEN1_BATTLE_ITEMS.includes(item.name)) {
        return {
          statusCode: 400,
          body: JSON.stringify({
            message: `${item.name} is not a Gen 1 battle item`
          }),
        };
      }

      const gen1Item = transformToGen1Item(item);

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(gen1Item),
      };
    }

    // Get all Gen 1 battle items
    const items = await itemsCollection
      .find({ name: { $in: GEN1_BATTLE_ITEMS } })
      .toArray();

    // Filter by category if provided
    let filteredItems = items.map(transformToGen1Item);

    if (category) {
      filteredItems = filteredItems.filter(item => item.category === category);
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        items: filteredItems,
        total: filteredItems.length,
      }),
    };

  } catch (err) {
    console.error('Error fetching Gen 1 Items:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: err.message }),
    };
  }
};

/**
 * Transform item data to Gen 1 battle item format
 * Categorizes items for easier filtering
 */
function transformToGen1Item(item) {
  // Determine item category
  let category = 'other';

  if (['potion', 'super-potion', 'hyper-potion', 'max-potion', 'full-restore'].includes(item.name)) {
    category = 'healing';
  } else if (['revive', 'max-revive'].includes(item.name)) {
    category = 'revival';
  } else if (['antidote', 'burn-heal', 'ice-heal', 'awakening', 'paralyze-heal', 'full-heal'].includes(item.name)) {
    category = 'status-heal';
  } else if (['x-attack', 'x-defend', 'x-speed', 'x-special', 'dire-hit', 'guard-spec'].includes(item.name)) {
    category = 'stat-boost';
  }

  // Extract heal amount for healing items
  let healAmount = null;
  if (category === 'healing') {
    const healMap = {
      'potion': 20,
      'super-potion': 50,
      'hyper-potion': 200,
      'max-potion': 999, // Full heal
      'full-restore': 999, // Full heal + status cure
    };
    healAmount = healMap[item.name] || null;
  }

  return {
    id: item.id,
    name: item.name,
    category,
    cost: item.cost || 0,
    effect: item.effect || item.short_effect || '',
    sprite: item.sprites?.default || null,

    // Gen 1 specific data
    gen1_data: {
      heal_amount: healAmount,
      usable_in_battle: true,
      generation: 1,
    }
  };
}
