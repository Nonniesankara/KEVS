import React from 'react';

function CandidateFilter({
  position,
  candidates,
  selectedCandidates,
  setSelectedCandidates,
}) {
  const handleChange = (e) => {
    setSelectedCandidates((prev) => ({
      ...prev,
      [position]: e.target.value,
    }));
  };

  return (
    <div className="form-group">
      <label>{position}</label>
      <select
        value={selectedCandidates[position] || ''}
        onChange={handleChange}
        required
      >
        <option value="">-- Select a {position} --</option>
        {candidates.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name} ({c.party})
          </option>
        ))}
      </select>
    </div>
  );
}

export default CandidateFilter;
