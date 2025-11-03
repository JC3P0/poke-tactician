// src/utils/capitalizeFirstLetter.js
const capitalizeFirstLetter = (string) => {
    return string ? string.charAt(0).toUpperCase() + string.slice(1) : '';
};

export default capitalizeFirstLetter;
