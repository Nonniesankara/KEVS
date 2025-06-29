import { useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';

function ConfirmPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { selectedCandidates, pollingStation, allCandidates } = location.state || {};

  useEffect(() => {
    if (!selectedCandidates || !pollingStation || !allCandidates) {
      navigate('/');
    }
  }, [selectedCandidates, pollingStation, allCandidates, navigate]);

  const renderVoteSummary = () => {
    return Object.entries(selectedCandidates).map(([position, candidateId]) => {
      const candidate = allCandidates.find(c => c.id === parseInt(candidateId));
      return (
        <div key={position} style={{ marginBottom: '1rem' }}>
          <p><strong>{position}:</strong> {candidate?.name} ({candidate?.party})</p>
        </div>
      );
    });
  };

  return (
    <div className="container">
      <h2 style={{ color: '#006400' }}>✅ Vote Submitted!</h2>
      <p>Thank you — your votes have been recorded successfully.</p>

      <div style={{ marginTop: '1rem' }}>
        <h3>Your Vote Summary:</h3>
        {renderVoteSummary()}
      </div>

      {pollingStation && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Polling Station Info:</h3>
          <p><strong>Name:</strong> {pollingStation.name}</p>
          <p><strong>Ward:</strong> {pollingStation.ward}</p>
        </div>
      )}

      <Link to="/" className="btn" style={{ marginTop: '2rem', display: 'inline-block' }}>
        Back to Home
      </Link>
    </div>
  );
}

export default ConfirmPage;
