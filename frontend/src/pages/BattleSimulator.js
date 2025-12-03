import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { optimizeBattle } from '../utils/api';

const BattleSimulator = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { team, bossTrainer } = location.state || {};

  const [selectedAlgorithm, setSelectedAlgorithm] = useState('dijkstra');
  const [playerLevel, setPlayerLevel] = useState(50);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [compareMode, setCompareMode] = useState(false);
  const [comparisonResults, setComparisonResults] = useState(null);

  // Run optimization when component loads
  useEffect(() => {
    if (!team || !bossTrainer) {
      navigate('/team-builder');
    }
  }, [team, bossTrainer, navigate]);

  const runOptimization = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await optimizeBattle(team, bossTrainer, selectedAlgorithm, playerLevel);
      setResult(response);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const runComparison = async () => {
    setLoading(true);
    setError(null);
    setCompareMode(true);

    try {
      const algorithms = ['greedy', 'dp', 'dijkstra'];
      const results = {};

      for (const algorithm of algorithms) {
        const response = await optimizeBattle(team, bossTrainer, algorithm, playerLevel);
        results[algorithm] = response;
      }

      setComparisonResults(results);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const AlgorithmBadge = ({ algorithm }) => {
    const badges = {
      greedy: { label: 'Greedy (Heap)', color: '#e74c3c', desc: 'Fast, suboptimal' },
      dp: { label: 'Dynamic Programming (HashTable)', color: '#3498db', desc: 'Optimal, memoized' },
      dijkstra: { label: 'Dijkstra (Graph)', color: '#2ecc71', desc: 'Optimal pathfinding' }
    };

    const badge = badges[algorithm] || badges.greedy;

    return (
      <div style={{
        background: badge.color,
        color: 'white',
        padding: '0.5rem 1rem',
        borderRadius: '8px',
        display: 'inline-block',
        marginBottom: '0.5rem'
      }}>
        <strong>{badge.label}</strong>
        <br />
        <small>{badge.desc}</small>
      </div>
    );
  };

  const ResultDisplay = ({ data, algorithm }) => {
    if (!data) return null;

    return (
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: '1.5rem',
        borderRadius: '12px',
        marginTop: '1rem'
      }}>
        <AlgorithmBadge algorithm={algorithm} />

        <div style={{ marginTop: '1rem' }}>
          <h3 style={{ color: '#ffcb05', marginBottom: '0.5rem' }}>Battle Result</h3>
          <p style={{ fontSize: '1.2rem', color: data.victory ? '#2ecc71' : '#e74c3c' }}>
            {data.victory ? '🎉 Victory!' : '💀 Defeat'}
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          <div>
            <p style={{ color: '#bdc3c7', fontSize: '0.9rem' }}>Total Damage</p>
            <p style={{ fontSize: '1.5rem', color: '#ffcb05' }}>{data.totalDamage}</p>
          </div>
          <div>
            <p style={{ color: '#bdc3c7', fontSize: '0.9rem' }}>Turns</p>
            <p style={{ fontSize: '1.5rem', color: '#ffcb05' }}>{data.turns}</p>
          </div>
          {data.statesExplored && (
            <div>
              <p style={{ color: '#bdc3c7', fontSize: '0.9rem' }}>States Explored</p>
              <p style={{ fontSize: '1.5rem', color: '#ffcb05' }}>{data.statesExplored}</p>
            </div>
          )}
          {data.cacheHitRate !== undefined && (
            <div>
              <p style={{ color: '#bdc3c7', fontSize: '0.9rem' }}>Cache Hit Rate</p>
              <p style={{ fontSize: '1.5rem', color: '#ffcb05' }}>{(data.cacheHitRate * 100).toFixed(1)}%</p>
            </div>
          )}
        </div>

        <div style={{ marginTop: '1.5rem' }}>
          <h4 style={{ color: '#ffcb05', marginBottom: '0.5rem' }}>Optimal Move Sequence</h4>
          <div style={{
            background: 'rgba(0,0,0,0.3)',
            padding: '1rem',
            borderRadius: '8px',
            maxHeight: '200px',
            overflowY: 'auto'
          }}>
            {data.moveSequence && data.moveSequence.length > 0 ? (
              <ol style={{ paddingLeft: '1.5rem', margin: 0 }}>
                {data.moveSequence.map((move, index) => (
                  <li key={index} style={{ padding: '0.3rem 0', color: '#ecf0f1' }}>
                    {move}
                  </li>
                ))}
              </ol>
            ) : (
              <p style={{ color: '#bdc3c7' }}>No moves available</p>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (!team || !bossTrainer) {
    return null;
  }

  return (
    <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
      <button
        onClick={() => navigate('/boss-selector', { state: { team } })}
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
        ← Back to Boss Selector
      </button>

      <h1 style={{ color: '#ffcb05', fontSize: '2.5rem', marginBottom: '1rem' }}>
        Battle Optimizer
      </h1>
      <p style={{ fontSize: '1.1rem', marginBottom: '2rem', color: '#bdc3c7' }}>
        CS_311 Extra Credit Project - Data Structures & Algorithms
      </p>

      {/* Configuration */}
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: '1.5rem',
        borderRadius: '12px',
        marginBottom: '2rem'
      }}>
        <h2 style={{ marginBottom: '1rem' }}>Battle Setup</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#bdc3c7' }}>
              Your Team: {team.length} Pokemon
            </label>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#bdc3c7' }}>
              Opponent: {bossTrainer}
            </label>
          </div>
        </div>

        <div style={{ marginTop: '1rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#bdc3c7' }}>
              Pokemon Level
            </label>
            <input
              type="number"
              min="1"
              max="100"
              value={playerLevel}
              onChange={(e) => setPlayerLevel(parseInt(e.target.value))}
              style={{
                width: '100%',
                padding: '0.5rem',
                fontSize: '1rem',
                borderRadius: '4px',
                border: 'none'
              }}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#bdc3c7' }}>
              Algorithm
            </label>
            <select
              value={selectedAlgorithm}
              onChange={(e) => setSelectedAlgorithm(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                fontSize: '1rem',
                borderRadius: '4px',
                border: 'none'
              }}
            >
              <option value="greedy">Greedy (Heap)</option>
              <option value="dp">Dynamic Programming (HashTable)</option>
              <option value="dijkstra">Dijkstra (Graph)</option>
            </select>
          </div>
        </div>

        <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
          <button
            onClick={runOptimization}
            disabled={loading}
            style={{
              flex: 1,
              padding: '1rem 2rem',
              fontSize: '1.1rem',
              cursor: loading ? 'not-allowed' : 'pointer',
              background: loading ? '#7f8c8d' : '#ffcb05',
              color: '#2c3e50',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 'bold'
            }}
          >
            {loading ? 'Running...' : 'Optimize Strategy'}
          </button>
          <button
            onClick={runComparison}
            disabled={loading}
            style={{
              flex: 1,
              padding: '1rem 2rem',
              fontSize: '1.1rem',
              cursor: loading ? 'not-allowed' : 'pointer',
              background: loading ? '#7f8c8d' : '#3498db',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 'bold'
            }}
          >
            {loading ? 'Comparing...' : 'Compare All Algorithms'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{
          background: '#e74c3c',
          color: 'white',
          padding: '1rem',
          borderRadius: '8px',
          marginBottom: '2rem'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Single Result Display */}
      {!compareMode && result && <ResultDisplay data={result} algorithm={selectedAlgorithm} />}

      {/* Comparison Display */}
      {compareMode && comparisonResults && (
        <div>
          <h2 style={{ color: '#ffcb05', marginBottom: '1rem' }}>Algorithm Comparison</h2>
          {Object.entries(comparisonResults).map(([algorithm, data]) => (
            <ResultDisplay key={algorithm} data={data} algorithm={algorithm} />
          ))}
        </div>
      )}
    </div>
  );
};

export default BattleSimulator;
