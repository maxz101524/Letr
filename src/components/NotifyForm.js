import React, { useState } from 'react';
import '../styles/NotifyForm.css';

const NotifyForm = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [message, setMessage] = useState('');

  const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateEmail(email)) {
      setStatus('error');
      setMessage('Please enter a valid email address');
      return;
    }

    setStatus('loading');
    setMessage('Submitting...');

    try {
      const response = await fetch('/api/subscribers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setStatus('success');
        setMessage(data.message || 'Thank you for your interest! We\'ll notify you when we launch.');
        setEmail('');
      } else {
        setStatus('error');
        setMessage(data.message || 'Something went wrong. Please try again.');
      }
    } catch (error) {
      setStatus('error');
      setMessage('Network error. Please check your connection and try again.');
    }
  };

  return (
    <div className="notify-form-container">
      <form onSubmit={handleSubmit} className="notify-form">
        <div className="input-group">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            className="email-input"
            disabled={status === 'loading' || status === 'success'}
          />
          <button 
            type="submit" 
            className="submit-button"
            disabled={status === 'loading' || status === 'success'}
          >
            {status === 'loading' ? 'Submitting...' : 'Notify Me'}
          </button>
        </div>
        {message && (
          <div className={`message ${status}`}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default NotifyForm; 