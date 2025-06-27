// src/pages/VotePage.js
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCandidates, submitVote } from '../services/api';
import CandidateFilter from './CandidateFilter';

function VotePage({ voter }) {
  const [selected, setSelected] = useState('');
  const [candidates, setCandidates] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!voter) return navigate('/login');
    if (voter.has_voted) {
      alert('You have already voted.');
      return navigate('/');
    }
    getCandidates().then(res => setCandidates(res.data));
  }, [voter]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await submitVote(voter.id, selected);
    navigate('/confirm');
  };

  return (
    <div>
      <h2>Cast Your Vote</h2>
      <CandidateFilter
        candidates={candidates}
        selected={selected}
        setSelected={setSelected}
      />
      <button onClick={handleSubmit} disabled={!selected}>Submit Vote</button>
    </div>
  );
}

export default VotePage;
