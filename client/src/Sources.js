import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Sources.css'; // Import Sources-specific styles

function Sources({ translations }) {
  const [urlList, setUrlList] = useState([]); // State to manage URLs
  const [inputValue, setInputValue] = useState(''); // State for the input field

  // Handler for adding a new URL
  const handleAddUrl = () => {
    if (inputValue.trim()) {
      setUrlList([...urlList, inputValue]); // Add the new URL to the list
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
        <p>Here you can add and remove sources</p>
      </div>
      
      {/* URL Management Section */}
      <div className="url-management">
        <input
          type="text"
          placeholder="Enter a source URL"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
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
