import React from "react";
import { Link } from 'react-router-dom';
import "./HomePage.css";

const HomePage = () => {
return (
<div className="home-page">
  <div className="content">
    <h1 className="title">
      Welcome to the Lang2LTL Web Demo
    </h1>
    <Link to="/demo" className="demo-link">Go to Demo Page</Link>
  </div>
</div>
);
};

export default HomePage