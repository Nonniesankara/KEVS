import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getCounties,
  getConstituencies,
  getWards,
  getPollingStations,
  getCandidates,
  submitVote,
} from '../services/api';
import CandidateFilter from './CandidateFilter';

function VotePage({ voter }) {
  const navigate = useNavigate();

  const [counties, setCounties] = useState([]);
  const [constituencies, setConstituencies] = useState([]);
  const [wards, setWards] = useState([]);
  const [stations, setStations] = useState([]);
  const [candidatesByPosition, setCandidatesByPosition] = useState({});

  const [selectedCounty, setSelectedCounty] = useState('');
  const [selectedConstituency, setSelectedConstituency] = useState('');
  const [selectedWard, setSelectedWard] = useState('');
  const [selectedStation, setSelectedStation] = useState('');

  const [selectedCandidates, setSelectedCandidates] = useState({});

  useEffect(() => {
    if (!voter) return navigate('/login');
    if (voter.has_voted) {
      alert('You have already voted.');
      return navigate('/');
    }
    getCounties().then(res => setCounties(res.data));
  }, [voter, navigate]);

  useEffect(() => {
    if (selectedCounty) {
      getConstituencies(selectedCounty).then(res => setConstituencies(res.data));
      setSelectedConstituency('');
      setWards([]);
      setStations([]);
      setCandidatesByPosition({});
      setSelectedCandidates({});
    } else {
      setConstituencies([]);
      setWards([]);
      setStations([]);
      setCandidatesByPosition({});
      setSelectedCandidates({});
    }
  }, [selectedCounty]);

  useEffect(() => {
    if (selectedConstituency) {
      getWards(selectedConstituency).then(res => setWards(res.data));
      setSelectedWard('');
      setStations([]);
      setCandidatesByPosition({});
      setSelectedCandidates({});
    } else {
      setWards([]);
      setStations([]);
      setCandidatesByPosition({});
      setSelectedCandidates({});
    }
  }, [selectedConstituency]);

  useEffect(() => {
    if (selectedWard) {
      getPollingStations(selectedWard).then(res => setStations(res.data));
      setSelectedStation('');
    } else {
      setStations([]);
      setSelectedStation('');
    }
  }, [selectedWard]);

  useEffect(() => {
    if (selectedCounty || selectedConstituency || selectedWard) {
      const positions = ['President', 'Governor', 'Senator', 'MP', 'MCA'];
      Promise.all(
        positions.map(position => {
          const params = { position };

          if (position === 'Governor' || position === 'Senator') {
            if (selectedCounty) params.countyId = selectedCounty;
          } else if (position === 'MP') {
            if (selectedConstituency) params.constituencyId = selectedConstituency;
          } else if (position === 'MCA') {
            if (selectedWard) params.wardId = selectedWard;
          }
          return getCandidates(params).then(res => ({
            position,
            candidates: res.data,
          }));
        })
      ).then(results => {
        const grouped = {};
        results.forEach(({ position, candidates }) => {
          if (candidates.length > 0) {
            grouped[position] = candidates;
          }
        });
        setCandidatesByPosition(grouped);
        setSelectedCandidates({});
      });
    } else {
      setCandidatesByPosition({});
      setSelectedCandidates({});
    }
  }, [selectedCounty, selectedConstituency, selectedWard]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const candidateIds = Object.values(selectedCandidates);
      await submitVote(voter.id, candidateIds);

      navigate('/confirm', {
        state: {
          selectedCandidates,
          pollingStation: stations.find(s => s.id === parseInt(selectedStation)),
          allCandidates: Object.values(candidatesByPosition).flat(),
        },
      });
    } catch (err) {
      console.error('Vote submission failed:', err);
      alert('Failed to submit your vote. Please try again.');
    }
  };

  return (
    <div className="vote-card animate-fade-in">
      <h2>Cast Your Vote</h2>

      <div className="form-group animate-slide-in">
        <label>Select County</label>
        <select value={selectedCounty} onChange={e => setSelectedCounty(e.target.value)}>
          <option value="">-- Select County --</option>
          {counties.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      {constituencies.length > 0 && (
        <div className="form-group animate-slide-in">
          <label>Select Constituency</label>
          <select value={selectedConstituency} onChange={e => setSelectedConstituency(e.target.value)}>
            <option value="">-- Select Constituency --</option>
            {constituencies.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
      )}

      {wards.length > 0 && (
        <div className="form-group animate-slide-in">
          <label>Select Ward</label>
          <select value={selectedWard} onChange={e => setSelectedWard(e.target.value)}>
            <option value="">-- Select Ward --</option>
            {wards.map(w => (
              <option key={w.id} value={w.id}>{w.name}</option>
            ))}
          </select>
        </div>
      )}

      {stations.length > 0 && (
        <div className="form-group animate-slide-in">
          <label>Select Polling Station</label>
          <select value={selectedStation} onChange={e => setSelectedStation(e.target.value)}>
            <option value="">-- Select Polling Station --</option>
            {stations.map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
      )}

      {Object.keys(candidatesByPosition).length > 0 && (
        <div className="animate-slide-in">
          <h3>Select One Candidate per Position</h3>
          {Object.entries(candidatesByPosition).map(([position, candidateList]) => (
            <CandidateFilter
              key={position}
              position={position}
              candidates={candidateList}
              selectedCandidates={selectedCandidates}
              setSelectedCandidates={setSelectedCandidates}
            />
          ))}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={Object.keys(candidatesByPosition).some(pos => !selectedCandidates[pos])}
        className="btn animate-slide-in"
      >
        Submit Vote
      </button>
    </div>
  );
}

export default VotePage;
