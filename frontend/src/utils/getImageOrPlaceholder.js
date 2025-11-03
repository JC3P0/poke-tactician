// src/utils/getImageOrPlaceholder.js

const placeholderImageUrl = 'https://raw.githubusercontent.com/JC3P0/misc_assets/main/Pokedex/noImg-2.png';

export const getImageOrPlaceholder = (spriteUrl) => {
  return spriteUrl ? spriteUrl : placeholderImageUrl;
};
