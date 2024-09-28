// src/SignUp.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './SignUp.css';  // Optional: Create a SignUp.css file for custom styling

function SignUp() {
  const [language, setLanguage] = useState('English');  // Use 'English' as the default selected language
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle sign-up logic here
    console.log('Preferred Language:', language);
    console.log('Email:', email);
    console.log('Password:', password);
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
        <div className="form-group">
          <label>Preferred Language:</label>
          {/* Dropdown for selecting the language */}
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            required
          >
            <option value="English">English</option>
            <option value="Spanish">Spanish</option>
            <option value="French">French</option>
            <option value="German">German</option>
            <option value="Chinese">Mandarin</option>
            <option value="Japanese">Japanese</option>
          </select>
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
        </div>
        <button type="submit">Sign Up</button>
        <p><Link to="/">Back to Home</Link></p>  {/* Link to go back to the home page */}
      </form>
    </div>
  );
}

export default SignUp;
