// src/pages/CandidateFilter.js
import React from 'react';

function CandidateFilter({ candidates, selected, setSelected }) {
  return (
    <select
      value={selected}
      onChange={e => setSelected(e.target.value)}
      required
    >
      <option value="">-- Select a candidate --</option>
      {candidates.map(c => (
        <option key={c.id} value={c.id}>
          {c.name} — {c.position} ({c.party})
        </option>
      ))}
    </select>
  );
}

export default CandidateFilter;
