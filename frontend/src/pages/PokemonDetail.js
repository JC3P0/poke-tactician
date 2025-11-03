import React, { useState } from 'react';
import { getImageOrPlaceholder } from '../utils/getImageOrPlaceholder';
import detail from '../styles/DetailedPage.module.css';
import useDetail from '../utils/hooks/useDetail';
import typeColors from '../utils/typeColors';

const PokemonDetail = () => {
  const { entity: pokemon, loading, error, favorites, toggleFavorite, navigate } = useDetail('pokemon');
  const [isShiny, setIsShiny] = useState(false);

  const statNames = {
    hp: "HP",
    attack: "ATT",
    defense: "DEF",
    special: "SPEC",  // Gen 1 unified Special stat
    speed: "SPD"
  };

  const toggleImage = () => {
    setIsShiny(!isShiny);
  };

  const convertWeightKgToLbs = (weightKg) => Math.round(weightKg * 2.20462);

  const convertHeightMToFtIn = (heightM) => {
    const totalInches = heightM * 39.3701;
    const feet = Math.floor(totalInches / 12);
    const inches = Math.round(totalInches % 12);
    return inches === 12 ? `${feet + 1}'0"` : `${feet}'${inches}"`;
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading Pokémon details: {error.message}</div>;

  const type1 = pokemon.types && pokemon.types[0];
  const type2 = pokemon.types && pokemon.types[1];
  const typeColor1 = typeColors[type1];
  const typeColor2 = type2 ? typeColors[type2] : '#2a3439';

  const backgroundImage = `linear-gradient(30deg, ${typeColor1} 12%, transparent 12.5%, transparent 87%, ${typeColor1} 87.5%, ${typeColor1}),
    linear-gradient(150deg, ${typeColor1} 12%, transparent 12.5%, transparent 87%, ${typeColor1} 87.5%, ${typeColor1}),
    linear-gradient(30deg, ${typeColor1} 12%, transparent 12.5%, transparent 87%, ${typeColor1} 87.5%, ${typeColor1}),
    linear-gradient(150deg, ${typeColor1} 12%, transparent 12.5%, transparent 87%, ${typeColor1} 87.5%, ${typeColor1}),
    linear-gradient(60deg, ${typeColor2} 25%, transparent 25.5%, transparent 75%, ${typeColor2} 75%, ${typeColor2}),
    linear-gradient(60deg, ${typeColor2} 25%, transparent 25.5%, transparent 75%, ${typeColor2} 75%, ${typeColor2})`;

  const cardStyle = {
    backgroundColor: '#556',
    backgroundImage: backgroundImage,
    backgroundSize: '80px 140px',
    backgroundPosition: '0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px',
  };

  // Gen 1 data has base_stats as an object, not an array
  const stats = pokemon.base_stats || {};
  const statArray = [
    { name: 'hp', base_stat: stats.hp },
    { name: 'attack', base_stat: stats.attack },
    { name: 'defense', base_stat: stats.defense },
    { name: 'special', base_stat: stats.special },
    { name: 'speed', base_stat: stats.speed }
  ];
  const maxStat = Math.max(...statArray.map((stat) => stat.base_stat));

  const weightKg = pokemon.weight / 10;
  const heightM = pokemon.height / 10;

  const weightLbs = convertWeightKgToLbs(weightKg);
  const heightFtIn = convertHeightMToFtIn(heightM);

  return (
    <div className={detail.detailContainer}>
      <div className={detail.detailCard} style={cardStyle}>
        <span className={detail.detailId}>#{pokemon.id}</span>
        <button
          className={`${detail.favoriteButton} ${
            favorites.some((f) => f._id === pokemon._id) ? detail.favorited : ''
          }`}
          onClick={() => toggleFavorite(pokemon._id, pokemon)}
        >
          {favorites.some((f) => f._id === pokemon._id) ? '❤️' : '♡'}
        </button>
        <button className={detail.backButton} onClick={() => navigate('/', { state: { tab: 'pokemon' } })}>
          <span>&#x2794;</span>
        </button>
        <button className={detail.shinyButton} onClick={toggleImage}>
          {isShiny ? 'Normal' : 'Shiny'}
        </button>
        <h1 className={detail.detailName}>{pokemon.name}</h1>
        <img
          className={detail.detailImage}
          src={getImageOrPlaceholder(isShiny ? pokemon.sprites.front_shiny : pokemon.sprites.front_default)}
          alt={pokemon.name}
        />
        <div className={detail.baseExperience}>Base Exp {pokemon.base_experience}</div>
        <div className={detail.pokemonTypes}>
          {type1 && (
            <span className={detail.pokemonType} style={{ backgroundColor: typeColors[type1] }}>
              {type1}
            </span>
          )}
          {type2 && (
            <span className={detail.pokemonType} style={{ backgroundColor: typeColors[type2], marginLeft: '10px' }}>
              {type2}
            </span>
          )}
        </div>
        <div className={detail.pokemonMeasurementsContainer}>
          <div className={detail.measurement}>
            <div className={detail.measurementValue}>{heightFtIn}</div>
            <div className={detail.measurementLabel}>Height</div>
          </div>
          <div className={detail.baseStatsTitle}>Base Stats</div>
          <div className={detail.measurement}>
            <div className={detail.measurementValue}>{weightLbs} lbs</div>
            <div className={detail.measurementLabel}>Weight</div>
          </div>
        </div>
        <div className={detail.pokemonStats}>
          {statArray.map((stat, index) => (
            <div key={index} className={detail.stat}>
              <span className={detail.statName}>{statNames[stat.name]}</span>
              <div className={detail.statBar} data-value={stat.base_stat}>
                <div className={detail.statBarFill} style={{ width: `${(stat.base_stat / maxStat) * 100}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PokemonDetail;
