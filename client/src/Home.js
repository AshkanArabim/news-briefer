import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home({ translations }) {
  return (
    <div className="home-container">
      <h1 className="home-title">{translations.homeTitle}</h1>
      <h1 className="home-subtitle">{translations.homeSubtitle}</h1>
      <div className="button-container">
        <Link to="/login">
          <button className="home-button">{translations.loginButton}</button>
        </Link>
        <Link to="/signup">
          <button className="home-button">{translations.signUpButton}</button>
        </Link>
        <Link to="/feed">
          <button className="home-button">{translations.feedButton}</button>
        </Link>
        {/* New Sources button */}
        <Link to="/sources">
          <button className="home-button">{translations.sourcesButton}</button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
