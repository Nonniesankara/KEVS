// src/pages/ResultsPage.js
import { useEffect, useState } from 'react';
import { getResults } from '../services/api';

function ResultsPage() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    getResults().then(res => setResults(res.data));
  }, []);

  return (
    <div className="container animate-fade-in">
      <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>Election Results</h2>
      <div className="results-card">
        <table className="results-table">
          <thead>
            <tr>
              <th>Candidate</th>
              <th>Position</th>
              <th>Party</th>
              <th>Votes</th>
            </tr>
          </thead>
          <tbody>
            {results.map(r => (
              <tr key={r.candidate_id}>
                <td>{r.candidate_name}</td>
                <td>{r.position}</td>
                <td>{r.party}</td>
                <td><strong>{r.vote_count}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ResultsPage;
