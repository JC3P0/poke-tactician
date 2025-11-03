import React from 'react';

// SearchSuggestions.js
const SearchSuggestions = ({ suggestions, onClick }) => {
    return (
      <div className="search-suggestions">
        {suggestions.map((suggestion) => (
          <div
            key={`${suggestion.type}-${suggestion.id}`}
            className="search-suggestion"
            onClick={() => onClick(suggestion)}
          >
            {suggestion.name}
          </div>
        ))}
      </div>
    );
  };


export default SearchSuggestions;
