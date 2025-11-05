import React from 'react';
import { useNavigate } from 'react-router-dom';

const BattleSimulator = () => {
  const navigate = useNavigate();

  return (
    <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
      <button onClick={() => navigate('/boss-selector')} style={{ marginBottom: '2rem', padding: '0.8rem 1.5rem', fontSize: '1rem', cursor: 'pointer' }}>
        ← Back to Boss Selector
      </button>

      <h1 style={{ color: '#ffcb05', fontSize: '2.5rem', marginBottom: '1rem' }}>
        Battle Simulator
      </h1>

      <div style={{ background: 'rgba(255,255,255,0.1)', padding: '2rem', borderRadius: '12px' }}>
        <h2 style={{ marginBottom: '1rem' }}>Coming Soon:</h2>
        <ul style={{ fontSize: '1.1rem', lineHeight: '2' }}>
          <li>🧮 Dynamic Programming Optimizer</li>
          <li>📊 Greedy Baseline Algorithm</li>
          <li>⚔️ Battle Visualization</li>
          <li>📈 Performance Comparison</li>
        </ul>
      </div>
    </div>
  );
};

export default BattleSimulator;
