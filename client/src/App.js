import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import SignUp from './SignUp';
import Feed from './Feed';
import './App.css';

function App() {
  // Create state to manage the selected language
  const [language, setLanguage] = useState('en');

  // Function to handle language changes
  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  // Define translations for each language
  const translations = {
    en: {
      homeTitle: 'Home',
      homeSubtitle: "What's happening today?",
      loginButton: 'Login',
      signUpButton: 'Sign Up',
      feedButton: 'Feed',
      feedContent: 'Here is what is happening today:',
    },
    es: {
      homeTitle: 'Inicio',
      homeSubtitle: '¿Qué está pasando hoy?',
      loginButton: 'Iniciar Sesión',
      signUpButton: 'Registrarse',
      feedButton: 'Noticias',
      feedContent: 'Aquí está lo que está pasando hoy:',
    },
    fr: {
      homeTitle: 'Accueil',
      homeSubtitle: 'Que se passe-t-il aujourd’hui ?',
      loginButton: 'Connexion',
      signUpButton: "S'inscrire",
      feedButton: 'Fil',
      feedContent: 'Voici ce qui se passe aujourd’hui :',
    },
  };

  return (
    <Router>
      <div className="App">
        {/* Global Language Dropdown */}
        <div className="language-dropdown">
          <select onChange={handleLanguageChange} value={language} className="language-select">
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="fr">Français</option>
          </select>
        </div>

        {/* Pass translations as a prop to each component */}
        <Routes>
          <Route path="/" element={<Home translations={translations[language]} />} />
          <Route path="/login" element={<Login translations={translations[language]} />} />
          <Route path="/signup" element={<SignUp translations={translations[language]} />} />
          <Route path="/feed" element={<Feed translations={translations[language]} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
