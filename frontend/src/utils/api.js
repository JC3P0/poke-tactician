import axios from 'axios';

// Create an axios instance with a base URL depending on the environment
const api = axios.create({
    baseURL: process.env.NODE_ENV === 'production' ? '/.netlify/functions' : 'http://localhost:8888/.netlify/functions'
});

// Function to fetch paginated data from a given URL
const fetchPaginatedData = async (url, limit = 100) => {
    let allData = [];
    let page = 1;
    let totalPages = 1;

    // Loop through all pages until all data is fetched
    while (page <= totalPages) {
        try {
            const response = await api.get(`${url}?page=${page}&limit=${limit}`);
            const data = response.data;
            allData = allData.concat(data.items || data.pokemon);
            totalPages = data.pages;
            page++;
        } catch (error) {
            console.error(`Error fetching data from ${url}:`, error);
            throw error;
        }
    }
    return allData;
};

export const fetchPokemon = async () => {
    return await fetchPaginatedData('/getGen1Pokemon');
};

export const fetchItems = async () => {
    return await fetchPaginatedData('/getGen1Items');
};
