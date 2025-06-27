import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5555',
});

export const login = ({ username, password }) =>
  API.post('/login', { username, password });

export const getCandidates = () =>
  API.get('/candidates');

export const submitVote = (voter_id, candidate_id) =>
  API.post('/submit-vote', { voter_id, candidate_id });

export const getResults = () =>
  API.get('/votes/count');
