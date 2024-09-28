// src/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home-container">  {/* Add a container div to center everything */}
      <h1 className="home-title">Home</h1>
      <h1 className="home-subtitle">What's happening today?</h1>
      <div className="button-container">
        {/* Create a button that navigates to the Login page */}
        <Link to="/login">
          <button className="home-button">Login</button>
        </Link>
        
        {/* Make Sign Up also look like a button */}
        <Link to="/signup">
          <button className="home-button">Sign Up</button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
