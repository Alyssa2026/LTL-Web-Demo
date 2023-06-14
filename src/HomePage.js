import React from "react";
import background from "./img/HomePic.png";
import { Link } from 'react-router-dom';
import "./HomePage.css"

const HomePage = () => {
  return (
    <div style={{
      backgroundImage: `url(${background})`,
      backgroundSize: '100% 100%',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'flex-start',
      alignItems: 'center'
    }}>
      <div style={{
        marginLeft: '3.6in', // Move the text to the left by 100 pixels
        marginBottom: '2.5in'
      }}>
        <h1 style={{ color: 'white' }}>
          Welcome to the Lang2LTL Web Demo
        </h1>
        <Link to="/demo" style={{ marginLeft: '210px', color: 'White' }}> Go to Demo Page</Link>
      </div>
    </div>
  );
};

export default HomePage;
