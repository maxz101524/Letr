// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import NotifyForm from './components/NotifyForm';
import AdminDashboard from './components/AdminDashboard';

function LandingPage() {
  return (
    <div className="landing-container">
      <div className="glass-card">
        <img src="/NetReach1.0.png" alt="NetReach Logo" className="logo" />
        <h1 className="title">NetReach</h1>
        <p className="subtitle">"Expand your network, not stress."</p>
        <p className="tagline">Helping you write personalized, authentic cold emails and cover letters in seconds.</p>
        <p className="coming-soon">Coming Soon<span className="dots">...</span></p>
        <NotifyForm />
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;


