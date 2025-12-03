import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { fetchBossTrainers } from '../utils/api';

const BossSelector = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const team = location.state?.team || [];

  const [bossTrainers, setBossTrainers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadBossTrainers = async () => {
      try {
        const trainers = await fetchBossTrainers();
        setBossTrainers(trainers);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    loadBossTrainers();
  }, []);

  const selectBoss = (bossId) => {
    navigate('/battle-simulator', {
      state: {
        team,
        bossTrainer: bossId
      }
    });
  };

  if (loading) {
    return (
      <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
        <p>Loading boss trainers...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
        <p>Error loading boss trainers: {error}</p>
        <button onClick={() => navigate('/team-builder')}>← Back to Team Builder</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
      <button
        onClick={() => navigate('/team-builder')}
        style={{
          marginBottom: '2rem',
          padding: '0.8rem 1.5rem',
          fontSize: '1rem',
          cursor: 'pointer',
          background: '#34495e',
          color: 'white',
          border: 'none',
          borderRadius: '8px'
        }}
      >
        ← Back to Team Builder
      </button>

      <h1 style={{ color: '#ffcb05', fontSize: '2.5rem', marginBottom: '1rem' }}>
        Choose Your Opponent
      </h1>

      <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
        Your team has {team.length} Pokemon. Choose a boss trainer to challenge!
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '2rem' }}>
        {Object.entries(bossTrainers).map(([bossId, boss]) => (
          <div
            key={bossId}
            onClick={() => selectBoss(bossId)}
            style={{
              background: 'rgba(255,255,255,0.1)',
              padding: '1.5rem',
              borderRadius: '12px',
              cursor: 'pointer',
              transition: 'all 0.3s',
              border: '2px solid transparent'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.border = '2px solid #ffcb05';
              e.currentTarget.style.transform = 'scale(1.02)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.border = '2px solid transparent';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            <h2 style={{ color: '#ffcb05', fontSize: '1.8rem', marginBottom: '0.5rem' }}>
              {boss.name}
            </h2>
            <h3 style={{ color: '#bdc3c7', fontSize: '1.2rem', marginBottom: '1rem' }}>
              {boss.title}
            </h3>
            <p style={{ fontSize: '1rem', lineHeight: '1.6', color: '#ecf0f1' }}>
              {boss.description}
            </p>
            <div style={{ marginTop: '1rem', padding: '0.5rem', background: 'rgba(255,203,5,0.2)', borderRadius: '8px' }}>
              <p style={{ fontSize: '0.9rem', color: '#ffcb05', textAlign: 'center' }}>
                Click to Battle! ⚔️
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BossSelector;
