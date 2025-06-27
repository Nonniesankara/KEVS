// src/pages/ResultsPage.js
import { useEffect, useState } from 'react';
import { getResults } from '../services/api';

function ResultsPage() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    getResults().then(res => setResults(res.data));
  }, []);

  return (
    <div>
      <h2>Election Results</h2>
      <table>
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
              <td>{r.vote_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultsPage;
