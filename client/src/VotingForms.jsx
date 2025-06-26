import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getVotingForms } from './api'; // Adjust the import based on your API file structure       
import './VotingForms.css'; // Optional: Add your CSS file for styling      
// Ensure you have the necessary API function to fetch voting forms
// Adjust the import based on your API file structure   

// Remove this function definition, as it is not used and contains React hooks which should not be inside a regular function

function VotingForms() {
    const [candidates, setCandidates] = useState([]);
    const [selectedCandidate, setSelectedCandidate] = useState('');
    const [message, setMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const navigate = useNavigate();
    useEffect(() => {
        fetch('http://localhost:5555/candidate')
            .then(response => response.json())
            .then(data => {
                setCandidates(data);
            })
            .catch(error => {
                console.error('Error fetching candidates:', error);
                setMessage('Failed to load candidates. Please try again later.');
            });
    }, []);

    const handleVote = async (e) => {
        e.preventDefault();
        if (!selectedCandidate) {
            setMessage('Please select a candidate to vote for.');
            return;
        }
        setIsSubmitting(true);
        try {
            const response = await fetch('http://localhost:5555/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ candidateId: selectedCandidate }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const result = await response.json();
            setMessage(result.message || 'Vote submitted successfully!');
            setSelectedCandidate('');
        } catch (error) {
            console.error('Error submitting vote:', error);
            setMessage('Failed to submit vote. Please try again later.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="voting-forms">
            <h1>Vote for Your Favorite Candidate</h1>
            {message && <p className="message">{message}</p>}
            <form onSubmit={handleVote}>
                <label htmlFor="candidate">Select a candidate:</label>
                <select
                    id="candidate"
                    value={selectedCandidate}
                    onChange={(e) => setSelectedCandidate(e.target.value)}
                >
                    <option value="">--Select a candidate--</option>
                    {candidates.map((candidate) => (
                        <option key={candidate.id} value={candidate.id}>
                            {candidate.name}
                        </option>
                    ))}
                </select>
                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? 'Submitting...' : 'Vote'}
                </button>
            </form>
            <button onClick={() => navigate('/results')}>View Results</button>
        </div>
    );
}

export default VotingForms;