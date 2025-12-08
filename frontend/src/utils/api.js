import axios from 'axios';

// Netlify functions for Pokemon/Items data (MongoDB)
const netlifyApi = axios.create({
    baseURL: process.env.NODE_ENV === 'production' ? '/.netlify/functions' : 'http://localhost:8888/.netlify/functions'
});

// AWS Lambda URL for battle optimizer (Python backend)
const LAMBDA_URL = 'https://q7qmizrsfpid27kz3lkm6eyffa0atzrv.lambda-url.us-east-1.on.aws/';

// Function to fetch paginated data from a given URL
const fetchPaginatedData = async (apiInstance, url, limit = 100) => {
    let allData = [];
    let page = 1;
    let totalPages = 1;

    // Loop through all pages until all data is fetched
    while (page <= totalPages) {
        try {
            const response = await apiInstance.get(`${url}?page=${page}&limit=${limit}`);
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
    return await fetchPaginatedData(netlifyApi, '/getGen1Pokemon');
};

export const fetchItems = async () => {
    return await fetchPaginatedData(netlifyApi, '/getGen1Items');
};

// Battle Optimizer API functions - Now using AWS Lambda!
export const fetchBossTrainers = async () => {
    try {
        const response = await axios.get(LAMBDA_URL);
        return response.data.bossTrainers;
    } catch (error) {
        console.error('Error fetching boss trainers:', error);
        throw error;
    }
};

export const optimizeBattle = async (playerTeam, opponent, algorithm = 'dijkstra', playerLevel = 50) => {
    try {
        // Map selectedMoves to moves for Lambda function
        const formattedPlayerTeam = playerTeam.map(pokemon => ({
            id: pokemon.id,
            name: pokemon.name,
            types: pokemon.types,
            base_stats: pokemon.base_stats,
            moves: pokemon.selectedMoves || pokemon.moves, // Use selectedMoves if available
            level: pokemon.level,
            dvs: pokemon.dvs,
            calculatedStats: pokemon.calculatedStats
        }));

        const payload = {
            playerTeam: formattedPlayerTeam,
            algorithm,
            playerLevel
        };

        // Add opponent (either boss trainer or custom team)
        if (typeof opponent === 'string') {
            payload.bossTrainer = opponent;
        } else {
            payload.opponentTeam = opponent;
        }

        const response = await axios.post(LAMBDA_URL, payload);
        return response.data;
    } catch (error) {
        console.error('Error optimizing battle:', error);
        throw error;
    }
};
