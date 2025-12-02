import axios from 'axios';

const apiRandomMovies = axios.create({
    baseURL: process.env.RANDOM_MOVIES_URL || 'http://127.0.0.1:5000',
    headers: {
        'Content-Type': 'application/json',
    },
});

const apiRecommendedMovies = axios.create({
    baseURL: process.env.RECOMMENDED_MOVIES_URL || 'http://127.0.0.1:5002',
    headers: {
        'Content-Type': 'application/json',
    },
})

const apiRating = axios.create({
    baseURL: process.env.RATING_URL || 'http://127.0.0.1:5001',
    headers: {
        'Content-Type': 'application/json',
    },
})


export { apiRandomMovies, apiRecommendedMovies, apiRating };