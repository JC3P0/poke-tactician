import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TeamBuilder from './pages/TeamBuilder';
import PokemonCustomizer from './pages/PokemonCustomizer';
import BossSelector from './pages/BossSelector';
import BattleSimulator from './pages/BattleSimulator';
import Results from './pages/Results';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/team-builder" element={<TeamBuilder />} />
        <Route path="/customize/:id" element={<PokemonCustomizer />} />
        <Route path="/boss-selector" element={<BossSelector />} />
        <Route path="/battle" element={<BattleSimulator />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
}

export default App;
