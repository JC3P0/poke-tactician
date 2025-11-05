import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import teamBuilderStyles from '../styles/TeamBuilder.module.css';
import typeColors from '../utils/typeColors';
import { getImageOrPlaceholder } from '../utils/getImageOrPlaceholder';

const TeamBuilder = () => {
  const [allPokemon, setAllPokemon] = useState([]);
  const [team, setTeam] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Fetch Gen 1 Pokemon from backend
  useEffect(() => {
    const fetchPokemon = async () => {
      try {
        // TODO: Replace with actual backend API endpoint
        // For now, use mock data or PokéAPI directly
        const response = await fetch('https://pokeapi.co/api/v2/pokemon?limit=151');
        const data = await response.json();

        // Fetch detailed info for each Pokemon
        const pokemonDetails = await Promise.all(
          data.results.map(async (pokemon) => {
            const res = await fetch(pokemon.url);
            const details = await res.json();
            return {
              id: details.id,
              name: details.name,
              types: details.types.map(t => t.type.name),
              sprites: details.sprites,
              base_stats: {
                hp: details.stats[0].base_stat,
                attack: details.stats[1].base_stat,
                defense: details.stats[2].base_stat,
                // Gen 1 uses unified Special stat (use Sp.Atk as base)
                special: details.stats[3].base_stat,
                speed: details.stats[5].base_stat
              }
            };
          })
        );

        setAllPokemon(pokemonDetails);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchPokemon();
  }, []);

  // Add Pokemon to team (max 6)
  const addToTeam = (pokemon) => {
    if (team.length >= 6) {
      alert('Your team is full! Remove a Pokemon first.');
      return;
    }

    if (team.some(p => p.id === pokemon.id)) {
      alert('This Pokemon is already on your team!');
      return;
    }

    // Add with default stats (will be customized later)
    const teamMember = {
      ...pokemon,
      level: 100, // Default level
      dvs: { hp: 15, attack: 15, defense: 15, special: 15, speed: 15 }, // Max DVs
      moves: [] // Will be set in customizer
    };

    setTeam([...team, teamMember]);
  };

  // Remove Pokemon from team
  const removeFromTeam = (pokemonId) => {
    setTeam(team.filter(p => p.id !== pokemonId));
  };

  // Navigate to customizer
  const customizePokemon = (pokemon) => {
    navigate(`/customize/${pokemon.id}`, { state: { pokemon, fromTeam: true } });
  };

  // Navigate to boss selector
  const proceedToBattle = () => {
    if (team.length === 0) {
      alert('Add at least one Pokemon to your team!');
      return;
    }
    navigate('/boss-selector', { state: { team } });
  };

  if (loading) return <div className={teamBuilderStyles.loading}>Loading Gen 1 Pokemon...</div>;
  if (error) return <div className={teamBuilderStyles.error}>Error: {error}</div>;

  return (
    <div className={teamBuilderStyles.container}>
      {/* Header */}
      <div className={teamBuilderStyles.header}>
        <button
          className={teamBuilderStyles.backButton}
          onClick={() => navigate('/')}
        >
          ← Home
        </button>
        <h1 className={teamBuilderStyles.title}>Build Your Team</h1>
        <button
          className={teamBuilderStyles.nextButton}
          onClick={proceedToBattle}
          disabled={team.length === 0}
        >
          Battle! →
        </button>
      </div>

      {/* Team Display (Top Section) */}
      <div className={teamBuilderStyles.teamSection}>
        <h2>Your Team ({team.length}/6)</h2>
        <div className={teamBuilderStyles.teamSlots}>
          {[0, 1, 2, 3, 4, 5].map((index) => {
            const pokemon = team[index];
            return (
              <div
                key={index}
                className={`${teamBuilderStyles.teamSlot} ${!pokemon ? teamBuilderStyles.empty : ''}`}
              >
                {pokemon ? (
                  <>
                    <img
                      src={getImageOrPlaceholder(pokemon.sprites?.front_default)}
                      alt={pokemon.name}
                      className={teamBuilderStyles.teamSprite}
                    />
                    <div className={teamBuilderStyles.teamInfo}>
                      <span className={teamBuilderStyles.teamName}>{pokemon.name}</span>
                      <span className={teamBuilderStyles.teamLevel}>Lv. {pokemon.level}</span>
                    </div>
                    <div className={teamBuilderStyles.teamActions}>
                      <button
                        className={teamBuilderStyles.customizeBtn}
                        onClick={() => customizePokemon(pokemon)}
                      >
                        ⚙️
                      </button>
                      <button
                        className={teamBuilderStyles.removeBtn}
                        onClick={() => removeFromTeam(pokemon.id)}
                      >
                        ✕
                      </button>
                    </div>
                  </>
                ) : (
                  <span className={teamBuilderStyles.emptyText}>Empty Slot</span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Pokemon Selection (Bottom Section) */}
      <div className={teamBuilderStyles.selectionSection}>
        <h2>Gen I Pokemon (151)</h2>
        <div className={teamBuilderStyles.pokemonGrid}>
          {allPokemon.map((pokemon) => {
            const isOnTeam = team.some(p => p.id === pokemon.id);
            const type1 = pokemon.types[0];
            const type2 = pokemon.types[1];

            return (
              <div
                key={pokemon.id}
                className={`${teamBuilderStyles.pokemonCard} ${isOnTeam ? teamBuilderStyles.onTeam : ''}`}
                onClick={() => !isOnTeam && addToTeam(pokemon)}
              >
                <div className={teamBuilderStyles.pokemonId}>#{pokemon.id}</div>
                <img
                  src={getImageOrPlaceholder(pokemon.sprites?.front_default)}
                  alt={pokemon.name}
                  className={teamBuilderStyles.pokemonSprite}
                />
                <h3 className={teamBuilderStyles.pokemonName}>{pokemon.name}</h3>
                <div className={teamBuilderStyles.pokemonTypes}>
                  <span
                    className={teamBuilderStyles.type}
                    style={{ backgroundColor: typeColors[type1] }}
                  >
                    {type1}
                  </span>
                  {type2 && (
                    <span
                      className={teamBuilderStyles.type}
                      style={{ backgroundColor: typeColors[type2] }}
                    >
                      {type2}
                    </span>
                  )}
                </div>
                {isOnTeam && (
                  <div className={teamBuilderStyles.onTeamBadge}>
                    ✓ On Team
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TeamBuilder;
