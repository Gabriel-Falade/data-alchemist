import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './navbar';
import Hero from './hero';
import Upload from './upload';
import Analytics from './analytics';
import Statistics from './statistics';
import Visualize from './visualize';
import WikiPage from './WikiPage';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Hero />} />

          <Route path="/upload" element={<Upload />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/statistics" element={<Statistics />} />
          <Route path="/visualize" element={<Visualize />} />
          <Route path="/wiki" element={<WikiPage />} />
        </Routes>
      </main>
    </div>
    
  );
}

export default App;