import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css';

function Login({ translations }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Email:', email);
    console.log('Password:', password);
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        {/* Updated Structure: Group Home and Login buttons */}
        <div className="button-group">
          {/* Home Button */}
          <Link to="/" className="home-button">
            {translations.homeTitle}
          </Link>
          
        </div>

        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {/* Login Button */}
          <button type="submit" className="login-button">
            {translations.loginButton}
          </button>
        </div>
        
      </form>
    </div>
  );
}

export default Login;
