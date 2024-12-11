// src/App.js
import React from 'react';
import './App.css';
import MapComponent from './MapComponent';
import heroImage from './hero2.jpg';

function App() {
  return (
    <div className="App">
      <div className="hero-container">
        {/* Use the imported image */}
        <img src={heroImage} alt="Wildfire" className="hero-image" />
        <div className="hero-text">
          <h1>FireSight</h1>
          <p></p>
        </div>
      </div>
      <MapComponent />
    </div>
  );
}

export default App;
