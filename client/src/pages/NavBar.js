// src/pages/Navbar.js
import { Link } from 'react-router-dom';
import flag from '../assets/kenya-flag.png';
import '../index.css'; // adjust import if needed

function Navbar() {
  return (
    <nav style={{
      display: 'flex',
      alignItems: 'center',
      padding: '1rem',
      background: '#fff',
      borderBottom: '1px solid #ddd'
    }}>
      <img
        src={flag}
        alt="Kenyan Flag"
        style={{ height: '30px', marginRight: '10px' }}
      />
      <h1 style={{ margin: 0, marginRight: '20px' }}>KEVS</h1>
      <Link to="/" style={{ marginRight: '15px' }}>Home</Link>
      <Link to="/login" style={{ marginRight: '15px' }}>Login</Link>
      <Link to="/results" style={{ marginRight: '15px' }}>Results</Link>
      <Link to="/help">Help</Link>
    </nav>
  );
}

export default Navbar;
