import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import SignUp from './SignUp';
import Feed from './Feed';
import Sources from './Sources'; // Import the Sources component
import './App.css';

function App() {
  const [language, setLanguage] = useState('en');

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const translations = {
    en: {
      homeTitle: 'Home',
      homeSubtitle: "What's happening today?",
      loginButton: 'Login',
      signUpButton: 'Sign Up',
      feedButton: 'Feed',
      sourcesButton: 'Sources',
      feedContent: 'Here is what is happening today:',
    },
    es: {
      homeTitle: 'Inicio',
      homeSubtitle: '¿Qué está pasando hoy?',
      loginButton: 'Iniciar Sesión',
      signUpButton: 'Registrarse',
      feedButton: 'Noticias',
      sourcesButton: 'Fuentes',
      feedContent: 'Aquí está lo que está pasando hoy:',
    },
    fr: {
      homeTitle: 'Accueil',
      homeSubtitle: 'Que se passe-t-il aujourd’hui ?',
      loginButton: 'Connexion',
      signUpButton: "S'inscrire",
      feedButton: 'Fil',
      sourcesButton: 'Sources',
      feedContent: 'Voici ce qui se passe aujourd’hui :',
    },
  };

  return (
    <Router>
      <div className="App">

        <Routes>
          <Route path="/" element={<Home translations={translations[language]} />} />
          <Route path="/login" element={<Login translations={translations[language]} />} />
          <Route path="/signup" element={<SignUp translations={translations[language]} />} />
          <Route path="/feed" element={<Feed translations={translations[language]} />} />
          <Route path="/sources" element={<Sources translations={translations[language]} />} /> {/* Add Sources Route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
