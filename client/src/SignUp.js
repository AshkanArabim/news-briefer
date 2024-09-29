import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './SignUp.css';

const apiUrl = 'http://127.0.0.1:5000/login';

function SignUp({ translations }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [formData, setFormData] = useState({"email": "", "password": "", "confirmPassword": ""}); // Initialize as empty object

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value // Use name attribute to identify the field
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    console.log('Form Data on Submit:', formData); // Log the formData here

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    // Create a single object for user credentials
    const userObject = {
      email: email,
      password: password
    };

    console.log('User Object:', JSON.stringify(userObject));

    // Make a POST request
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userObject),
    })
      .then((response) => {
        console.log('Response Status:', response.status); 
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Success Data:', data); 
        setMessage('Signup successful!');
      })
      .catch((error) => {
        console.error('Fetch Error:', error);
        setMessage(`Signup failed. Error: ${error.message}`);
      });
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        {/* Home Button */}
        <div className="button-group">
          <Link to="/" className="home-button">
            {translations ? translations.homeTitle : 'Home'}
          </Link>
        </div>
        <h2>{translations ? translations.signUpButton : 'Sign Up'}</h2>

        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            name="email" // Add name attribute
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              handleChange(e);
            }}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            name="password" // Add name attribute
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              handleChange(e);
            }}
            required
          />
        </div>
        <div className="form-group">
          <label>Confirm Password:</label>
          <input
            type="password"
            name="confirmPassword" // Add name attribute
            value={confirmPassword}
            onChange={(e) => {
              setConfirmPassword(e.target.value);
              handleChange(e);
            }}
            required
          />
        </div>

        {/* Display the message */}
        {message && <p className="message">{message}</p>}

        {/* Sign Up Button */}
        <button type="submit" className="signup-button">
          {translations ? translations.signUpButton : 'Sign Up'}
        </button>
      </form>
    </div>
  );
}

export default SignUp;