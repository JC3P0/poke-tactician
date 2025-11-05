import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const BossSelector = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const team = location.state?.team || [];

  return (
    <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
      <button onClick={() => navigate('/team-builder')} style={{ marginBottom: '2rem', padding: '0.8rem 1.5rem', fontSize: '1rem', cursor: 'pointer' }}>
        ← Back to Team Builder
      </button>

      <h1 style={{ color: '#ffcb05', fontSize: '2.5rem', marginBottom: '1rem' }}>
        Choose Your Opponent
      </h1>

      <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
        Your team has {team.length} Pokemon. Choose a boss trainer to challenge!
      </p>

      <div style={{ background: 'rgba(255,255,255,0.1)', padding: '2rem', borderRadius: '12px' }}>
        <h2 style={{ marginBottom: '1rem' }}>Coming Soon:</h2>
        <ul style={{ fontSize: '1.1rem', lineHeight: '2' }}>
          <li>🎮 8 Gym Leaders (Brock, Misty, Lt. Surge, Erika, etc.)</li>
          <li>⚡ Elite Four (Lorelei, Bruno, Agatha, Lance)</li>
          <li>👑 Champion Blue (Gary)</li>
        </ul>
      </div>
    </div>
  );
};

export default BossSelector;
