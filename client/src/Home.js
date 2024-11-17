import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import store from './store';

function Home({ translations }) {
  const token = store.getState().user.token
  const loggedIn = token != null && token.length > 0;

  return (
    <div className="home-container">
      <h1 className="home-title">Newsbridge</h1>
      {/* <h1 className="home-subtitle">{translations.homeSubtitle}</h1> */}
      <div className="button-container">
        {loggedIn ? (
          <>
            <Link to="/feed">
              <button className="home-button">{translations.feedButton}</button>
            </Link>
            <Link to="/sources">
              <button className="home-button">{translations.sourcesButton}</button>
            </Link>
          </>
        ) : (
          <>
            <Link to="/login">
              <button className="home-button">{translations.loginButton}</button>
            </Link>
            <Link to="/signup">
              <button className="home-button">{translations.signUpButton}</button>
            </Link>
          </>
        )}

        <a href="https://github.com/AshkanArabim/newsbridge">
          <button className="home-button gh-button">Star on GitHub</button>
        </a>
      </div>
    </div>
  );
}

export default Home;
