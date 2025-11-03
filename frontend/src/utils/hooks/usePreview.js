import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getItemsFromIndexedDB,
  getPokemonFromIndexedDB,
  getItemFavoritesFromIndexedDB,
  getPokemonFavoritesFromIndexedDB,
  toggleItemFavoriteInIndexedDB,
  togglePokemonFavoriteInIndexedDB,
} from '../indexedDB';

const usePreview = (type) => {
  const [entities, setEntities] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (type === 'item') {
          const items = await getItemsFromIndexedDB();
          if (items.length === 0) {
            // Redirect to root if data is not loaded
            navigate('/');
            return;
          }
          setEntities(items);
          setFavorites(await getItemFavoritesFromIndexedDB());
        } else if (type === 'pokemon') {
          const pokemon = await getPokemonFromIndexedDB();
          if (pokemon.length === 0) {
            // Redirect to root if data is not loaded
            navigate('/');
            return;
          }
          setEntities(pokemon);
          setFavorites(await getPokemonFavoritesFromIndexedDB());
        }
      } catch (e) {
        setError(e);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [type, navigate]);

  const handleNavigate = (id) => {
    navigate(`/${type === 'item' ? 'items' : 'pokemon'}/${id}`);
  };

  const toggleFavorite = async (_id, entity) => {
    if (type === 'item') {
      await toggleItemFavoriteInIndexedDB(_id, entity);
      setFavorites(await getItemFavoritesFromIndexedDB());
    } else if (type === 'pokemon') {
      await togglePokemonFavoriteInIndexedDB(_id, entity);
      setFavorites(await getPokemonFavoritesFromIndexedDB());
    }
  };

  const toggleShowCategory = (category) => {
    setActiveCategory(category);
  };

  return {
    entities,
    favorites,
    activeCategory,
    handleNavigate,
    toggleFavorite,
    toggleShowCategory,
    loading,
    error,
  };
};

export default usePreview;
