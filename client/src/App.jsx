// src/App.jsx
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import VotePage from './pages/VotePage';
import ResultsPage from './pages/ResultsPage';
import ConfirmPage from './pages/ConfirmPage';
import HelpPage from './pages/HelpPage';
import NavBar from './pages/NavBar';
import AboutPage from './pages/AboutPage';

function App() {
  const [voter, setVoter] = useState(null);

  return (
    <Router>
      <NavBar />
      <div className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage setVoter={setVoter} />} />
          <Route path="/vote" element={<VotePage voter={voter} />} />
          <Route path="/confirm" element={<ConfirmPage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/help" element={<HelpPage />} />
          <Route path="*" element={<Navigate to="/" />} />
          <Route path="/about" element={<AboutPage/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
