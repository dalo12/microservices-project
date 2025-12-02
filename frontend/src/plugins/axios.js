import axios from 'axios';

const apiRandomMovies = axios.create({
    baseURL: import.meta.env.RANDOM_MOVIES_URL || 'http://127.0.0.1:5000',
    headers: {
        'Content-Type': 'application/json',
    },
});

const apiRecommendedMovies = axios.create({
    baseURL: import.meta.env.RECOMMENDED_MOVIES_URL || 'http://127.0.0.1:5002',
    headers: {
        'Content-Type': 'application/json',
    },
})

const apiRating = axios.create({
    baseURL: import.meta.env.RATING_URL || 'http://127.0.0.1:5001',
    headers: {
        'Content-Type': 'application/json',
    },
})


export { apiRandomMovies, apiRecommendedMovies, apiRating };