import './App.css';
import { MapContainer, TileLayer } from 'react-leaflet';
import { useState } from 'react';
import { useRef } from 'react';
import 'leaflet/dist/leaflet.css';
import * as React from 'react';
import { BrowserRouter as Router, Link, Route, useHistory, } from 'react-router-dom';

// Alerts localhost when button is clicked to convert--> may be useful for when we implement ltl 
function clickMe(){
  alert('Convert has been clicked')
}

// Screen where the demo will be hosted
function Demo() {
  const [center, setCenter] = useState({lat: 41.8268, lng: -71.4025})
  const ZOOM_LEVEL = 16;
  const mapRef = useRef()
  const url =  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

// Implementing API/Logos
  return (
    <div className="backround-color" >

      <h1 style={{ fontSize: 20, marginLeft: '2in', marginTop: '1in'  }}>
        Enter Natural Language Command:
      </h1>
     
      <h2 style={{ fontSize: 20, marginLeft: '2in' }}>
        <input type= "text"></input>
        <button onClick={clickMe}>
          Convert to LTL
        </button>
        </h2>

      <h3 style={{ fontSize: 20, marginLeft: '2in'}}>
        LTL Output: 
      </h3>

      <h4 style={{ fontSize: 20, marginLeft: '2in'}}>
        <input type= "text"></input>
      </h4>

      <space>
      </space>
    
      <div>
        <MapContainer center = {center} zoom= {ZOOM_LEVEL} ref = {mapRef}>
            <TileLayer 
            url = {url} />

        </MapContainer>
      </div>
   </div>  
  );
}

export default Demo;
