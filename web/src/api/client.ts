import axios from 'axios';

// Use environment variable if available, otherwise default to the production Cloud URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://sulkysubject37-plan-f-api.hf.space';

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});
