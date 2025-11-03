import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const useSearch = (items, pokemon) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredItems, setFilteredItems] = useState([]);
  const [filteredPokemon, setFilteredPokemon] = useState([]);
  const navigate = useNavigate();

  const handleSearch = (e) => {
    const { value } = e.target;
    const validatedValue = value.replace(/[^a-zA-Z]/g, '').substring(0, 20);
    setSearchTerm(validatedValue);

    if (validatedValue === '') {
      setFilteredItems([]);
      setFilteredPokemon([]);
      return;
    }

    // Filter Pokémon and add a type property for differentiation
    const filteredPokemonList = pokemon
      .filter((p) =>
        p.name.toLowerCase().startsWith(validatedValue.toLowerCase())
      )
      .map((p) => ({ ...p, type: 'pokemon' })); // Add type property

    // Filter items and add a type property for differentiation
    const filteredItemsList = items
      .filter((i) =>
        i.name.toLowerCase().startsWith(validatedValue.toLowerCase())
      )
      .map((i) => ({ ...i, type: 'item' })); // Add type property

    setFilteredPokemon(filteredPokemonList);
    setFilteredItems(filteredItemsList);
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchTerm(suggestion.name);

    // Determine navigation path based on suggestion type
    if (suggestion.type === 'item') {
      navigate(`/items/${suggestion.id}`);
    } else if (suggestion.type === 'pokemon') {
      navigate(`/pokemon/${suggestion.id}`);
    }
  };

  return {
    searchTerm,
    filteredItems,
    filteredPokemon,
    handleSearch,
    handleSuggestionClick,
  };
};

export default useSearch;
