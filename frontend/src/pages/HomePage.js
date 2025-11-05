import React from 'react';
import { useNavigate } from 'react-router-dom';
import homeStyles from '../styles/HomePage.module.css';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className={homeStyles.homeContainer}>
      <div className={homeStyles.heroSection}>
        <h1 className={homeStyles.title}>
          <span className={homeStyles.poke}>POKE</span>
          <span className={homeStyles.tactician}>-TACTICIAN</span>
        </h1>
        <p className={homeStyles.subtitle}>Gen 1 Battle Optimizer Using Dynamic Programming</p>

        <div className={homeStyles.description}>
          <p>Can your team beat the legendary trainers of Kanto?</p>
          <p>Build your dream Gen 1 team and challenge iconic Gym Leaders, the Elite Four, and Champion Blue!</p>
        </div>

        <div className={homeStyles.featureGrid}>
          <div className={homeStyles.featureCard}>
            <span className={homeStyles.featureIcon}>⚡</span>
            <h3>Authentic Gen 1</h3>
            <p>DVs (0-15), unified Special stat, speed-based crits, and all the quirky Gen 1 mechanics</p>
          </div>

          <div className={homeStyles.featureCard}>
            <span className={homeStyles.featureIcon}>🎯</span>
            <h3>Dynamic Programming</h3>
            <p>Optimal battle strategies calculated using advanced algorithms</p>
          </div>

          <div className={homeStyles.featureCard}>
            <span className={homeStyles.featureIcon}>🏆</span>
            <h3>13 Boss Trainers</h3>
            <p>Challenge all 8 Gym Leaders, Elite Four, and Champion Blue from Red/Blue</p>
          </div>

          <div className={homeStyles.featureCard}>
            <span className={homeStyles.featureIcon}>📊</span>
            <h3>Battle Visualization</h3>
            <p>Watch turn-by-turn animated battles with detailed analytics</p>
          </div>
        </div>

        <div className={homeStyles.ctaSection}>
          <button
            className={homeStyles.primaryButton}
            onClick={() => navigate('/team-builder')}
          >
            Build Your Team
          </button>
          <button
            className={homeStyles.secondaryButton}
            onClick={() => navigate('/boss-selector')}
          >
            View Boss Trainers
          </button>
        </div>

        <div className={homeStyles.gen1Info}>
          <h3>Why Generation I?</h3>
          <ul>
            <li><strong>Historical Significance:</strong> The original Pokemon experience that started it all</li>
            <li><strong>Unique Mechanics:</strong> DVs instead of IVs, no Sp.Atk/Sp.Def split, quirky type bugs</li>
            <li><strong>15 Types:</strong> No Dark, Steel, or Fairy - pure classic Pokemon</li>
            <li><strong>Nostalgia:</strong> Battle the trainers that defined a generation</li>
          </ul>
        </div>
      </div>

      <footer className={homeStyles.homeFooter}>
        <p>Built for Data Structures & Algorithms Course</p>
        <p className={homeStyles.disclaimer}>
          Pokemon © Nintendo, Game Freak, The Pokemon Company.
          This is a fan-made educational project.
        </p>
      </footer>
    </div>
  );
};

export default HomePage;
