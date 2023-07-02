import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import DemoPage from './DemoPage';

const App = () => {
  return (
    // Creates a path from HomePage to DemoPage when link in HomePage is clicked
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/demo" element={<DemoPage />} />
      </Routes>
    </Router>
  );
};

export default App;
