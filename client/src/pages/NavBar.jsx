// src/pages/NavBar.jsx
import { Link } from 'react-router-dom';
import flag from '../assets/kenya-flag.png';
import '../index.css';

function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img src={flag} alt="Kenyan Flag" className="flag" />
        <h1 className="logo">KEVS</h1>
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/login" className="nav-link">Login</Link>
        <Link to="/results" className="nav-link">Results</Link>
        <Link to="/help" className="nav-link">Help</Link>
      </div>
      
    </nav>
  );
}

export default NavBar;
