import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { getImageOrPlaceholder } from '../utils/getImageOrPlaceholder';
import { savePokemonToTeam } from '../utils/indexedDB';
import customizerStyles from '../styles/PokemonCustomizer.module.css';
import typeColors from '../utils/typeColors';

const PokemonCustomizer = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  // Get Pokemon from route state or fetch it
  const [pokemon, setPokemon] = useState(location.state?.pokemon || null);
  const [loading, setLoading] = useState(!location.state?.pokemon);

  // Customizable stats (Gen 1)
  const [level, setLevel] = useState(100);
  const [dvs, setDvs] = useState({
    hp: 15,
    attack: 15,
    defense: 15,
    special: 15,
    speed: 15
  });
  const [moves, setMoves] = useState([null, null, null, null]);
  const [errors, setErrors] = useState([]);

  // Available moves (placeholder - will fetch from backend later)
  // TODO: Fetch actual Gen 1 moves from backend API
  const availableMoves = [
    { id: 1, name: 'Tackle', type: 'normal', power: 40 },
    { id: 2, name: 'Thunderbolt', type: 'electric', power: 90 },
    { id: 3, name: 'Ice Beam', type: 'ice', power: 90 },
    { id: 4, name: 'Earthquake', type: 'ground', power: 100 },
  ];

  useEffect(() => {
    if (!pokemon) {
      // Fetch Pokemon details if not passed via state
      const fetchPokemon = async () => {
        try {
          const res = await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);
          const data = await res.json();
          setPokemon({
            id: data.id,
            name: data.name,
            types: data.types.map(t => t.type.name),
            sprites: data.sprites,
            base_stats: {
              hp: data.stats[0].base_stat,
              attack: data.stats[1].base_stat,
              defense: data.stats[2].base_stat,
              special: data.stats[3].base_stat,
              speed: data.stats[5].base_stat
            }
          });
          setLoading(false);
        } catch (err) {
          console.error('Error fetching Pokemon:', err);
          setLoading(false);
        }
      };
      fetchPokemon();
    }
  }, [id, pokemon]);

  // Calculate actual stats using Gen 1 formulas
  // Source: Bulbapedia - "Stat" article (Gen 1 formulas)
  const calculateStat = (base, dv, statName) => {
    if (statName === 'hp') {
      // HP Formula: floor(((Base + DV) * 2 + 63) * Level / 100) + Level + 10
      return Math.floor(((base + dv) * 2 + 63) * level / 100) + level + 10;
    } else {
      // Other Stats: floor(((Base + DV) * 2 + 63) * Level / 100) + 5
      return Math.floor(((base + dv) * 2 + 63) * level / 100) + 5;
    }
  };

  const handleDvChange = (stat, value) => {
    const numValue = Math.min(15, Math.max(0, parseInt(value) || 0));
    setDvs({ ...dvs, [stat]: numValue });
  };

  const handleMoveSelect = (slotIndex, moveId) => {
    const selectedMove = availableMoves.find(m => m.id === parseInt(moveId));
    const newMoves = [...moves];
    newMoves[slotIndex] = selectedMove;
    setMoves(newMoves);
    setErrors([]); // Clear errors when user makes changes
  };

  const validateForm = () => {
    const validationErrors = [];

    // Check if all 4 moves are selected
    const selectedMoves = moves.filter(m => m !== null);
    if (selectedMoves.length < 4) {
      validationErrors.push(`You must select exactly 4 moves (${selectedMoves.length}/4 selected)`);
    }

    // Check for duplicate moves
    const moveIds = selectedMoves.map(m => m?.id).filter(id => id);
    const uniqueMoveIds = new Set(moveIds);
    if (moveIds.length !== uniqueMoveIds.size) {
      validationErrors.push('You cannot select the same move twice!');
    }

    return validationErrors;
  };

  const handleSave = async () => {
    // Validate form
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Save customized Pokemon and return to team builder
    const customizedPokemon = {
      ...pokemon,
      level,
      dvs,
      moves: moves.filter(m => m !== null).map(m => m.name), // Save move names for battle optimizer
      selectedMoves: moves.filter(m => m !== null), // Keep full move objects for display
      calculatedStats: {
        hp: calculateStat(pokemon.base_stats.hp, dvs.hp, 'hp'),
        attack: calculateStat(pokemon.base_stats.attack, dvs.attack, 'attack'),
        defense: calculateStat(pokemon.base_stats.defense, dvs.defense, 'defense'),
        special: calculateStat(pokemon.base_stats.special, dvs.special, 'special'),
        speed: calculateStat(pokemon.base_stats.speed, dvs.speed, 'speed')
      }
    };

    // Save to IndexedDB
    const success = await savePokemonToTeam(customizedPokemon);

    if (success) {
      console.log('Pokemon saved to team:', customizedPokemon);
      navigate('/team-builder');
    } else {
      setErrors(['Failed to save Pokemon. Team may be full (max 6 Pokemon).']);
    }
  };

  if (loading) return <div className={customizerStyles.loading}>Loading...</div>;
  if (!pokemon) return <div className={customizerStyles.error}>Pokemon not found</div>;

  const type1 = pokemon.types[0];
  const type2 = pokemon.types[1];

  return (
    <div className={customizerStyles.container}>
      {/* Header */}
      <div className={customizerStyles.header}>
        <button
          className={customizerStyles.backButton}
          onClick={() => navigate('/team-builder')}
        >
          ← Back to Team
        </button>
        <h1 className={customizerStyles.title}>Customize {pokemon.name}</h1>
        <button
          className={customizerStyles.saveButton}
          onClick={handleSave}
        >
          Save & Return
        </button>
      </div>

      {/* Validation Errors */}
      {errors.length > 0 && (
        <div style={{
          background: 'rgba(231, 76, 60, 0.2)',
          border: '2px solid #e74c3c',
          borderRadius: '8px',
          padding: '1rem',
          margin: '1rem 0',
          color: '#e74c3c'
        }}>
          <strong>⚠️ Please fix these errors:</strong>
          <ul style={{ margin: '0.5rem 0 0 0', paddingLeft: '1.5rem' }}>
            {errors.map((error, i) => (
              <li key={i}>{error}</li>
            ))}
          </ul>
        </div>
      )}

      <div className={customizerStyles.content}>
        {/* Pokemon Display */}
        <div className={customizerStyles.pokemonDisplay}>
          <div className={customizerStyles.spriteContainer}>
            <img
              src={getImageOrPlaceholder(pokemon.sprites?.front_default)}
              alt={pokemon.name}
              className={customizerStyles.sprite}
            />
          </div>
          <h2 className={customizerStyles.pokemonName}>{pokemon.name}</h2>
          <div className={customizerStyles.types}>
            <span
              className={customizerStyles.type}
              style={{ backgroundColor: typeColors[type1] }}
            >
              {type1}
            </span>
            {type2 && (
              <span
                className={customizerStyles.type}
                style={{ backgroundColor: typeColors[type2] }}
              >
                {type2}
              </span>
            )}
          </div>
        </div>

        {/* Customization Panel */}
        <div className={customizerStyles.customizationPanel}>
          {/* Level Selector */}
          <div className={customizerStyles.section}>
            <h3>Level</h3>
            <input
              type="range"
              min="1"
              max="100"
              value={level}
              onChange={(e) => setLevel(parseInt(e.target.value))}
              className={customizerStyles.slider}
            />
            <span className={customizerStyles.levelDisplay}>{level}</span>
          </div>

          {/* DV Inputs (Gen 1: 0-15) */}
          <div className={customizerStyles.section}>
            <h3>DVs (Determinant Values) - Gen 1</h3>
            <p className={customizerStyles.hint}>Range: 0-15 (15 is max)</p>
            <div className={customizerStyles.dvGrid}>
              {['hp', 'attack', 'defense', 'special', 'speed'].map(stat => (
                <div key={stat} className={customizerStyles.dvInput}>
                  <label>{stat.toUpperCase()}</label>
                  <input
                    type="number"
                    min="0"
                    max="15"
                    value={dvs[stat]}
                    onChange={(e) => handleDvChange(stat, e.target.value)}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Calculated Stats Display */}
          <div className={customizerStyles.section}>
            <h3>Calculated Stats (Level {level})</h3>
            <div className={customizerStyles.statsDisplay}>
              {['hp', 'attack', 'defense', 'special', 'speed'].map(stat => (
                <div key={stat} className={customizerStyles.statRow}>
                  <span className={customizerStyles.statName}>{stat.toUpperCase()}</span>
                  <span className={customizerStyles.statValue}>
                    {calculateStat(pokemon.base_stats[stat], dvs[stat], stat)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Move Selection */}
          <div className={customizerStyles.section}>
            <h3>Moves (Select up to 4)</h3>
            <div className={customizerStyles.movesGrid}>
              {[0, 1, 2, 3].map(index => (
                <div key={index} className={customizerStyles.moveSlot}>
                  <label>Move {index + 1}</label>
                  <select
                    value={moves[index]?.id || ''}
                    onChange={(e) => handleMoveSelect(index, e.target.value)}
                    className={customizerStyles.moveSelect}
                  >
                    <option value="">-- Select Move --</option>
                    {availableMoves.map(move => (
                      <option key={move.id} value={move.id}>
                        {move.name} ({move.type}, {move.power} power)
                      </option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PokemonCustomizer;
