import { useEffect, useState } from 'react';
import { getItemsFromIndexedDB, saveItemsToIndexedDB, getPokemonFromIndexedDB, savePokemonToIndexedDB } from '../indexedDB';
import { fetchItems, fetchPokemon } from '../api';
import { useLocation } from 'react-router-dom';

const useFetchData = () => {
  const [items, setItems] = useState([]);
  const [pokemon, setPokemon] = useState([]);
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      if (location.pathname.startsWith('/items') || location.pathname === '/') {
        let cachedItems = await getItemsFromIndexedDB();
        if (cachedItems.length === 0) {
          const itemsData = await fetchItems();
          await saveItemsToIndexedDB(itemsData);
          setItems(itemsData);
        } else {
          setItems(cachedItems);
        }
      }

      if (location.pathname.startsWith('/pokemon') || location.pathname === '/') {
        let cachedPokemon = await getPokemonFromIndexedDB();
        if (cachedPokemon.length === 0) {
          const pokemonData = await fetchPokemon();
          await savePokemonToIndexedDB(pokemonData);
          setPokemon(pokemonData);
        } else {
          setPokemon(cachedPokemon);
        }
      }
    };

    fetchData();
  }, [location.pathname]);

  return { items, pokemon };
};

export default useFetchData;
