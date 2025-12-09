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
        <p className={homeStyles.subtitle}>Gen 1 Battle Optimizer</p>


        <div className={homeStyles.featureGrid}>
          <div className={homeStyles.featureCard}>
            <span className={homeStyles.featureIcon}>⚡</span>
            <h3>Authentic Gen 1</h3>
            <p>DVs (0-15), unified Special stat, speed-based crits</p>
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

      </div>

      <footer className={homeStyles.homeFooter}>
        <p>Built for Data Structures & Algorithms Course</p>
      </footer>
    </div>
  );
};

export default HomePage;
