// src/App.js
import React from 'react';
import './App.css';

function App() {
  return (
    <div className="landing-container">
      <div className="glass-card">
        <img src="/NetReach1.0.png" alt="NetReach Logo" className="logo" />
        <h1 className="title">NetReach</h1>
        <p className="subtitle">"Expand your network, not stress."</p>
        <p className="tagline">Helping you write personalized, authentic cold emails and cover letters in seconds.</p>
        <p className="coming-soon">Coming Soon<span className="dots">...</span></p>
        <button className="cta-button">Notify Me</button>
      </div>
    </div>
  );
}

export default App;


