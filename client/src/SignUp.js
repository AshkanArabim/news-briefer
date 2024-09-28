import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './SignUp.css'; // Use the SignUp-specific CSS file

function SignUp({ translations }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Email:', email);
    console.log('Password:', password);
    console.log('Confirm Password:', confirmPassword);
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        {/* Home Button */}
        <div className="button-group">
          <Link to="/" className="home-button">
            {translations.homeTitle}
          </Link>
        </div>
        <h2>{translations ? translations.signUpButton : 'Sign Up'}</h2>




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
        <div className="form-group">
          <label>Confirm Password:</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        {/* Sign Up Button */}
        <button type="submit" className="signup-button">
          {translations ? translations.signUpButton : 'Sign Up'}
        </button>



      </form>
    </div>
  );
}

export default SignUp;
