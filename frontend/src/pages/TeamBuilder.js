import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchPokemon } from '../utils/api';
import { loadTeam, removePokemonFromTeam, clearTeam } from '../utils/indexedDB';
import teamBuilderStyles from '../styles/TeamBuilder.module.css';
import typeColors from '../utils/typeColors';
import { getImageOrPlaceholder } from '../utils/getImageOrPlaceholder';

const TeamBuilder = () => {
  const [allPokemon, setAllPokemon] = useState([]);
  const [team, setTeam] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Fetch Gen 1 Pokemon from MongoDB backend
  useEffect(() => {
    const loadPokemon = async () => {
      try {
        const pokemonData = await fetchPokemon();
        setAllPokemon(pokemonData);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    loadPokemon();
  }, []);

  // Load saved team from IndexedDB
  useEffect(() => {
    const loadSavedTeam = async () => {
      try {
        const savedTeam = await loadTeam();
        setTeam(savedTeam);
      } catch (err) {
        console.error('Error loading team from IndexedDB:', err);
      }
    };

    loadSavedTeam();
  }, []);

  // Navigate to customizer when clicking a Pokemon
  const selectPokemon = (pokemon) => {
    if (team.length >= 6 && !team.some(p => p.id === pokemon.id)) {
      alert('Your team is full! Remove a Pokemon first.');
      return;
    }

    if (team.some(p => p.id === pokemon.id)) {
      alert('This Pokemon is already on your team! Edit it from the team section above.');
      return;
    }

    // Navigate to customizer to set level, DVs, and moves
    navigate(`/customize/${pokemon.id}`, { state: { pokemon } });
  };

  // Remove Pokemon from team and IndexedDB
  const removeFromTeam = async (pokemonId) => {
    await removePokemonFromTeam(pokemonId);
    setTeam(team.filter(p => p.id !== pokemonId));
  };

  // Clear entire team
  const handleClearTeam = async () => {
    if (window.confirm('Are you sure you want to clear your entire team?')) {
      await clearTeam();
      setTeam([]);
    }
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
        <div style={{ display: 'flex', gap: '1rem' }}>
          {team.length > 0 && (
            <button
              className={teamBuilderStyles.clearButton}
              onClick={handleClearTeam}
              style={{
                background: '#e74c3c',
                color: 'white',
                padding: '0.8rem 1.5rem',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '1rem',
                fontWeight: 'bold'
              }}
            >
              Clear Team
            </button>
          )}
          <button
            className={teamBuilderStyles.nextButton}
            onClick={proceedToBattle}
            disabled={team.length === 0}
          >
            Battle! →
          </button>
        </div>
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
                onClick={() => !isOnTeam && selectPokemon(pokemon)}
                style={{ cursor: isOnTeam ? 'not-allowed' : 'pointer' }}
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
