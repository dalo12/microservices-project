import axios from 'axios';

const api = axios.create({
    baseURL: 'http://172.19.0.2:5000/',
    headers:{
        'Content-Type': 'application/json',
    },
});


export {api};