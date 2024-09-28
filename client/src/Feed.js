import React from 'react';
import { Link } from 'react-router-dom';
import './Feed.css';

function Feed({ translations }) {
  return (
    <div className="feed-container">
      {/* Home button at the top center */}
      <div className="home-button-container">
        <Link to="/">
          <button className="home-button">{translations ? translations.homeTitle : 'Home'}</button>
        </Link>
      </div>
      
      {/* Feed page content */}
      <h1 className="feed-title">{translations ? translations.feedButton : 'Feed Page'}</h1>
      {/* Use the translations prop for the paragraph content */}
      <p>{translations ? translations.feedContent : 'Here is what is happening today:'}</p>
    </div>
  );
}

export default Feed;
