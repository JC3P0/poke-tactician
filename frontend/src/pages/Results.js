import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { optimizeBattle } from '../utils/api';

const Results = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { team, bossTrainer } = location.state || {};

  const [results, setResults] = useState({
    greedy: null,
    dp: null,
    dijkstra: null
  });
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    if (!team || !bossTrainer) {
      setErrors(['Missing team or boss trainer data']);
      setLoading(false);
      return;
    }

    const runAllAlgorithms = async () => {
      setLoading(true);
      const newResults = {};
      const newErrors = [];

      // Run all 3 algorithms in parallel
      const algorithms = ['greedy', 'dp', 'dijkstra'];

      try {
        const promises = algorithms.map(async (algorithm) => {
          try {
            const result = await optimizeBattle(team, bossTrainer, algorithm, 50);
            return { algorithm, result };
          } catch (error) {
            console.error(`Error running ${algorithm}:`, error);
            return { algorithm, error: error.message };
          }
        });

        const settled = await Promise.all(promises);

        settled.forEach(({ algorithm, result, error }) => {
          if (error) {
            newErrors.push(`${algorithm}: ${error}`);
          } else {
            newResults[algorithm] = result;
          }
        });

        setResults(newResults);
        setErrors(newErrors);
        setLoading(false);
      } catch (error) {
        setErrors([`Failed to run algorithms: ${error.message}`]);
        setLoading(false);
      }
    };

    runAllAlgorithms();
  }, [team, bossTrainer]);

  const downloadResults = () => {
    const data = {
      team: team.map(p => ({ id: p.id, name: p.name, level: p.level, moves: p.moves })),
      bossTrainer,
      results,
      timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date().getTime();
    a.download = `battle-results-${bossTrainer}-${timestamp}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!team || !bossTrainer) {
    return (
      <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
        <h1>Error: No Battle Data</h1>
        <p>Please start from Team Builder</p>
        <button onClick={() => navigate('/team-builder')}>ê Back to Team Builder</button>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh', textAlign: 'center' }}>
        <h1 style={{ color: '#ffcb05', fontSize: '2.5rem', marginBottom: '2rem' }}>Running Battle Simulations...</h1>
        <div style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>
          <div>î Greedy Algorithm (Heap-based)</div>
          <div>>‡ Dynamic Programming (Hash Table memoization)</div>
          <div>=˙ Dijkstra's Algorithm (Graph shortest path)</div>
        </div>
        <div style={{ marginTop: '2rem', fontSize: '1rem', opacity: 0.7 }}>
          This may take a few seconds...
        </div>
      </div>
    );
  }

  const hasResults = Object.values(results).some(r => r !== null);

  return (
    <div style={{ padding: '2rem', color: 'white', background: '#2c3e50', minHeight: '100vh' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <button
          onClick={() => navigate('/boss-selector', { state: { team } })}
          style={{
            padding: '0.8rem 1.5rem',
            fontSize: '1rem',
            cursor: 'pointer',
            background: '#34495e',
            color: 'white',
            border: 'none',
            borderRadius: '8px'
          }}
        >
          ê Back to Boss Selection
        </button>

        <h1 style={{ color: '#ffcb05', fontSize: '2.5rem', margin: 0 }}>
          Battle Results
        </h1>

        {hasResults && (
          <button
            onClick={downloadResults}
            style={{
              padding: '0.8rem 1.5rem',
              fontSize: '1rem',
              cursor: 'pointer',
              background: '#27ae60',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 'bold'
            }}
          >
            =Â Download Results (JSON)
          </button>
        )}
      </div>

      {/* Team Info */}
      <div style={{ background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '8px', marginBottom: '2rem' }}>
        <h3>Your Team ({team.length} Pokemon) vs. {bossTrainer}</h3>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {team.map(p => (
            <span key={p.id} style={{ background: 'rgba(255,203,5,0.2)', padding: '0.5rem 1rem', borderRadius: '4px' }}>
              {p.name} (Lv. {p.level})
            </span>
          ))}
        </div>
      </div>

      {/* Errors */}
      {errors.length > 0 && (
        <div style={{
          background: 'rgba(231, 76, 60, 0.2)',
          border: '2px solid #e74c3c',
          borderRadius: '8px',
          padding: '1rem',
          marginBottom: '2rem'
        }}>
          <strong>† Errors:</strong>
          <ul>
            {errors.map((error, i) => (
              <li key={i}>{error}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Results Grid */}
      {hasResults && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem' }}>
          {['greedy', 'dp', 'dijkstra'].map(algorithm => {
            const result = results[algorithm];
            if (!result) return null;

            const algorithmNames = {
              greedy: 'Greedy (Heap)',
              dp: 'Dynamic Programming (Hash Table)',
              dijkstra: "Dijkstra's Algorithm (Graph)"
            };

            const algorithmIcons = {
              greedy: 'î',
              dp: '>‡',
              dijkstra: '=˙'
            };

            return (
              <div key={algorithm} style={{
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '12px',
                padding: '1.5rem',
                border: '2px solid rgba(255,203,5,0.3)'
              }}>
                <h2 style={{ color: '#ffcb05', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span>{algorithmIcons[algorithm]}</span>
                  {algorithmNames[algorithm]}
                </h2>

                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>
                    <strong>Result:</strong> {result.victory ? ' Victory!' : 'L Defeat'}
                  </div>
                  <div><strong>Total Damage:</strong> {result.totalDamage}</div>
                  <div><strong>Turns:</strong> {result.turns}</div>
                  {result.cacheHits !== undefined && (
                    <div><strong>Cache Hits:</strong> {result.cacheHits} (DP optimization)</div>
                  )}
                  {result.statesExplored !== undefined && (
                    <div><strong>States Explored:</strong> {result.statesExplored}</div>
                  )}
                </div>

                <div>
                  <strong>Move Sequence:</strong>
                  <div style={{
                    maxHeight: '200px',
                    overflowY: 'auto',
                    background: 'rgba(0,0,0,0.3)',
                    padding: '0.5rem',
                    borderRadius: '4px',
                    marginTop: '0.5rem',
                    fontSize: '0.9rem'
                  }}>
                    {result.moveSequence && result.moveSequence.length > 0 ? (
                      result.moveSequence.map((move, i) => (
                        <div key={i}>{i + 1}. {move}</div>
                      ))
                    ) : (
                      <div>No moves recorded</div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Comparison Table */}
      {hasResults && (
        <div style={{ marginTop: '2rem', background: 'rgba(255,255,255,0.1)', borderRadius: '12px', padding: '1.5rem' }}>
          <h2 style={{ color: '#ffcb05', marginBottom: '1rem' }}>Algorithm Comparison</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid rgba(255,203,5,0.5)' }}>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Algorithm</th>
                <th style={{ padding: '0.75rem', textAlign: 'center' }}>Result</th>
                <th style={{ padding: '0.75rem', textAlign: 'center' }}>Damage</th>
                <th style={{ padding: '0.75rem', textAlign: 'center' }}>Turns</th>
                <th style={{ padding: '0.75rem', textAlign: 'center' }}>Special Stats</th>
              </tr>
            </thead>
            <tbody>
              {['greedy', 'dp', 'dijkstra'].map(algorithm => {
                const result = results[algorithm];
                if (!result) return null;

                const algorithmNames = {
                  greedy: 'Greedy',
                  dp: 'Dynamic Programming',
                  dijkstra: 'Dijkstra'
                };

                return (
                  <tr key={algorithm} style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                    <td style={{ padding: '0.75rem', fontWeight: 'bold' }}>{algorithmNames[algorithm]}</td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      {result.victory ? '' : 'L'}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>{result.totalDamage}</td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>{result.turns}</td>
                    <td style={{ padding: '0.75rem', textAlign: 'center', fontSize: '0.9rem' }}>
                      {result.cacheHits !== undefined && `Cache: ${result.cacheHits}`}
                      {result.statesExplored !== undefined && `States: ${result.statesExplored}`}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Results;
