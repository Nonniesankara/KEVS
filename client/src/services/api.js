import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5555',
});

// ---------------- AUTH ----------------

// Login
export const login = ({ username, password }) =>
  API.post('/login', { username, password });

// ---------------- CANDIDATES ----------------

// Get all candidates
export const getCandidates = () => API.get('/candidates');

// ✅ Grouped by position: President, Governor, etc.
export const getCandidatesGrouped = () => API.get('/candidates/grouped');

// ---------------- VOTING ----------------

// ✅ Submit multiple votes in one request
// Expects: { voter_id: Number, candidate_ids: [id1, id2, ...] }
export const submitVote = (voter_id, candidate_ids) =>
  API.post('/vote', { voter_id, candidate_ids });

// Get vote counts per candidate
export const getResults = () => API.get('/votes/count');

// ---------------- LOCATION DATA ----------------

// Counties
export const getCounties = () => API.get('/counties');

// Constituencies by County
export const getConstituencies = (countyId) =>
  API.get(`/constituencies/by_county/${countyId}`);

// Wards by Constituency
export const getWards = (constituencyId) =>
  API.get(`/wards/by_constituency/${constituencyId}`);

// Polling Stations by Ward
export const getPollingStations = (wardId) =>
  API.get(`/pollingstations/by_ward/${wardId}`);
