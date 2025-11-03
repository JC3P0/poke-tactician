import React from 'react';
import pokemonPage from '../styles/PreviewPage.module.css';
import BaseLayout from '../utils/BaseLayout';
import usePreview from '../utils/hooks/usePreview';
import renderPokemonCategory from '../utils/renderPokemonCategory';

const PokemonPage = () => {
  const {
    entities: pokemon,
    favorites: pokemonFavorites,
    activeCategory: activePokemonCategory,
    handleNavigate,
    toggleFavorite: togglePokemonFavorite,
    toggleShowCategory: toggleShowPokemonByGeneration,
  } = usePreview('pokemon');

  return (
    <BaseLayout>
      <div className={pokemonPage.previewContainer}>
        <div className={pokemonPage.categoryButtons}>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'all' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('all')}>Show All Pokémon</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen1' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen1')}>Gen I</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen2' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen2')}>Gen II</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen3' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen3')}>Gen III</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen4' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen4')}>Gen IV</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen5' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen5')}>Gen V</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen6' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen6')}>Gen VI</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen7' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen7')}>Gen VII</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen8' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen8')}>Gen VIII</button>
          <button className={`${pokemonPage.categoryButton} ${activePokemonCategory === 'gen9' ? pokemonPage.active : ''}`} onClick={() => toggleShowPokemonByGeneration('gen9')}>Gen IX</button>
        </div>
        <div className={pokemonPage.previewList}>
          {renderPokemonCategory({
            activePokemonCategory,
            pokemon,
            favorites: pokemonFavorites,
            toggleFavorite: togglePokemonFavorite,
            handleNavigate,
          })}
        </div>
      </div>
    </BaseLayout>
  );
};

export default PokemonPage;
