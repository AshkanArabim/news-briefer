import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Sources.css'; // Import Sources-specific styles
import store from "./store"
import { BACKEND_URL } from './vars';

function Sources({ translations }) {
  const [urlList, setUrlList] = useState([]); // State to manage URLs
  const [inputValue, setInputValue] = useState(''); // State for the input field

  // Handler for adding a new URL
  const handleAddUrl = async () => {
    if (inputValue.trim()) {
      setUrlList([...urlList, inputValue]); // Add the new URL to the list
      
      // add to the backend database
      await fetch(`${BACKEND_URL}/add-source`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: store.getState().user.token,
          source: inputValue.trim()
        })
      })
      
      setInputValue(''); // Clear the input field
    }
  };

  // Handler for removing a specific URL from the list
  const handleRemoveUrl = (index) => {
    setUrlList(urlList.filter((_, i) => i !== index)); // Remove the URL at the specified index
  };

  return (
    <div className="sources-container">
      {/* Home button */}
      <div className="button-container">
        <Link to="/">
          <button className="home-button">{translations ? translations.homeTitle : 'Home'}</button>
        </Link>
      </div>

      {/* Centered text */}
      <div className="main-text">
        <h1>Sources</h1>
      </div>
      
      {/* URL Management Section */}
      <div className="url-management">
        <input
          type="text"
          placeholder="Enter a source URL"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Enter') handleAddUrl(); }}

          className="url-input"
        />

        <div className="url-buttons">
          {/* Add URL Button */}
          <button className="home-button" onClick={handleAddUrl}>
            add
            {translations ? translations.addUrlButton : 'Add URL'}
          </button>
        </div>
      </div>

      {/* Display the list of URLs */}
      <div className="url-list">
        <h2>{translations ? translations.urlListTitle : 'Source List:'}</h2>
        <ul>
          {urlList.map((url, index) => (
            <li key={index} className="url-item">
              {url}
              {/* Remove button for each URL */}
              <button className="home-button" onClick={() => handleRemoveUrl(index)}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Sources;
