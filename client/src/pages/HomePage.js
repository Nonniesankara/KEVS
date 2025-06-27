// src/pages/HomePage.js
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <h1>Welcome to KEVS</h1>
      <p>
        Secure voting for Kenyan military personnel and persons with disabilities.
      </p>
      <Link to="/login" className="btn">Login to Vote</Link>
      <Link to="/results" className="btn">View Results</Link>
    </div>
  );
}

export default HomePage;
