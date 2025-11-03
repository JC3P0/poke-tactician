// src/utils/hooks/useDetail.js
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  getItemByIdFromIndexedDB,
  getPokemonByIdFromIndexedDB,
  getItemFavoritesFromIndexedDB,
  getPokemonFavoritesFromIndexedDB,
  toggleItemFavoriteInIndexedDB,
  togglePokemonFavoriteInIndexedDB,
} from '../indexedDB';

const useDetail = (type) => {
  const { id } = useParams();
  const [entity, setEntity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [favorites, setFavorites] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        let data;
        if (type === 'item') {
          data = await getItemByIdFromIndexedDB(id);
        } else if (type === 'pokemon') {
          data = await getPokemonByIdFromIndexedDB(id);
        }

        if (!data) {
          navigate('/');
          return;
        }

        setEntity(data);
        setLoading(false);
      } catch (error) {
        console.error(`Error fetching ${type}:`, error);
        setError(error);
        setLoading(false);
        navigate('/');
      }
    };

    const fetchFavorites = async () => {
      try {
        let favoritesData;
        if (type === 'item') {
          favoritesData = await getItemFavoritesFromIndexedDB();
        } else if (type === 'pokemon') {
          favoritesData = await getPokemonFavoritesFromIndexedDB();
        }
        setFavorites(favoritesData);
      } catch (error) {
        console.error('Error fetching favorites:', error);
      }
    };

    fetchData();
    fetchFavorites();
  }, [id, type, navigate]);

  const toggleFavorite = async (_id, entity) => {
    if (type === 'item') {
      await toggleItemFavoriteInIndexedDB(_id, entity);
      setFavorites(await getItemFavoritesFromIndexedDB());
    } else if (type === 'pokemon') {
      await togglePokemonFavoriteInIndexedDB(_id, entity);
      setFavorites(await getPokemonFavoritesFromIndexedDB());
    }
  };

  return {
    entity,
    loading,
    error,
    favorites,
    toggleFavorite,
    navigate,
  };
};

export default useDetail;
