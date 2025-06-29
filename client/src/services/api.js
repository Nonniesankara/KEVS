import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5555',
});

// ---------------- AUTH ----------------

// Login
export const login = ({ username, password }) =>
  API.post('/login', { username, password });

// ---------------- LOCATIONS ----------------

// Get all counties
export const getCounties = () => API.get('/counties');

// Get constituencies by county
export const getConstituencies = (countyId) =>
  API.get(`/constituencies/by_county/${countyId}`);

// Get wards by constituency
export const getWards = (constituencyId) =>
  API.get(`/wards/by_constituency/${constituencyId}`);

// Get polling stations by ward
export const getPollingStations = (wardId) =>
  API.get(`/pollingstations/by_ward/${wardId}`);

// ---------------- CANDIDATES ----------------

// Get candidates with optional filters (county, constituency, ward)
export const getCandidates = (filters) =>
  API.get('/candidates', { params: filters });

// Get all candidates grouped by position
export const getCandidatesGrouped = () =>
  API.get('/candidates/grouped');

// ---------------- VOTING ----------------

// Submit a vote
export const submitVote = (voterId, candidateIds) =>
  API.post('/vote', {
    voter_id: voterId,
    candidate_ids: candidateIds,
  });

// ---------------- RESULTS ----------------

// Get vote counts per candidate
export const getResults = () =>
  API.get('/votes/count');
