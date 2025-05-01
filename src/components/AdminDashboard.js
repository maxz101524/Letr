import React, { useState, useEffect } from 'react';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [subscriberData, setSubscriberData] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // Load subscriber data if authenticated
  useEffect(() => {
    if (token) {
      setIsAuthenticated(true);
      fetchSubscriberData();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchSubscriberData = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/subscribers', {
        headers: {
          'x-auth-token': token
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSubscriberData(data);
        setError('');
      } else {
        // Token invalid or expired
        setIsAuthenticated(false);
        localStorage.removeItem('authToken');
        setToken(null);
        setError('Session expired. Please login again.');
      }
    } catch (err) {
      setError('Error fetching data. Please try again.');
    }
    setLoading(false);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('authToken', data.token);
        setToken(data.token);
        setIsAuthenticated(true);
        setUsername('');
        setPassword('');
        fetchSubscriberData();
      } else {
        setError(data.message || 'Login failed');
        setLoading(false);
      }
    } catch (err) {
      setError('Server error. Please try again.');
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setIsAuthenticated(false);
    setSubscriberData(null);
  };

  // Format dates for display
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (loading) {
    return <div className="admin-container"><div className="loading">Loading...</div></div>;
  }

  if (!isAuthenticated) {
    return (
      <div className="admin-container">
        <div className="admin-card">
          <h2>Admin Login</h2>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="login-button">
              Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>NetReach Admin Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>

      <div className="dashboard-card summary-card">
        <h2>Subscriber Summary</h2>
        <div className="stats-container">
          <div className="stat-item">
            <h3>Total Subscribers</h3>
            <p className="stat-value">{subscriberData?.total || 0}</p>
          </div>
          <div className="stat-item">
            <h3>Last 30 Days</h3>
            <p className="stat-value">
              {subscriberData?.dailyStats?.reduce((sum, day) => sum + day.count, 0) || 0}
            </p>
          </div>
        </div>
      </div>

      {subscriberData?.dailyStats?.length > 0 && (
        <div className="dashboard-card">
          <h2>Daily Signups (Last 30 Days)</h2>
          <div className="chart-container">
            {subscriberData.dailyStats.map((day) => (
              <div className="chart-bar" key={day._id}>
                <div 
                  className="bar" 
                  style={{ 
                    height: `${Math.max(20, day.count * 30)}px` 
                  }}
                >
                  <span className="bar-value">{day.count}</span>
                </div>
                <div className="bar-label">{day._id.slice(5)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="dashboard-card">
        <h2>Subscriber List</h2>
        {subscriberData?.subscribers?.length > 0 ? (
          <div className="subscriber-table-container">
            <table className="subscriber-table">
              <thead>
                <tr>
                  <th>Email</th>
                  <th>Date Joined</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {subscriberData.subscribers.map((sub) => (
                  <tr key={sub._id}>
                    <td>{sub.email}</td>
                    <td>{formatDate(sub.createdAt)}</td>
                    <td>{sub.referralSource}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="no-data">No subscribers yet.</p>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard; 