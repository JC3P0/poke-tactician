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

        <div className={homeStyles.description}>
          <p>Build your optimal Pokemon team and test strategies against legendary trainers.</p>
          <p>Uses advanced algorithms (Greedy, Dynamic Programming, Dijkstra) to find the best battle approach.</p>
          <p>Authentic Gen 1 mechanics with DVs, unified Special stat, and speed-based critical hits.</p>
        </div>

        <div className={homeStyles.ctaSection}>
          <button
            className={homeStyles.primaryButton}
            onClick={() => navigate('/team-builder')}
          >
            Build Your Team
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
