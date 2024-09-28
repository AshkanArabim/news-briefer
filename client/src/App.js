// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import SignUp from './SignUp';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Use Routes instead of Switch for React Router v6 */}
        <Routes>
          <Route path="/" element={<Home />} />   {/* Update component syntax */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
