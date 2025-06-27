// src/pages/ConfirmPage.js
import { Link } from 'react-router-dom';

function ConfirmPage() {
  return (
    <div>
      <h2>Vote Submitted!</h2>
      <p>Thank you — your vote has been recorded.</p>
      <Link to="/">Back to Home</Link>
    </div>
  );
}

export default ConfirmPage;
