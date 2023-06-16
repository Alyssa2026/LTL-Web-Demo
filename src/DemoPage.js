import './DemoPage.css';
import { MapContainer, TileLayer } from 'react-leaflet';
import { useState } from 'react';
import { useRef } from 'react';
import 'leaflet/dist/leaflet.css';
import genProp from './PropositionGen/Proposition.py'
import $ from 'jquery'; // Import jQuery library

// Screen where the demo will be hosted
function Demo() {
  const [center, setCenter] = useState({lat: 41.8268, lng: -71.4025})
  const ZOOM_LEVEL = 16;
  const mapRef = useRef()
  const url =  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  
  // When clicked, this will get the bounds, parse and filter the location selected
  function clickMe(){
    if (mapRef.current) {
      // Get Bounds
      const map = mapRef.current;
      const bounds = map.getBounds();
      const minLat = bounds.getSouth();
      const maxLat = bounds.getNorth();
      const minLng = bounds.getWest();
      const maxLng = bounds.getEast();
      // reate URL
      const osmUrl = `https://api.openstreetmap.org/api/0.6/map?bbox=${minLng},${minLat},${maxLng},${maxLat}`;
      // function to get genProp and processes the URL
      console.log('hello')
      $.ajax({
        url: 'Proposition.py', // Replace with the appropriate endpoint on your server
        type: 'text',
        data: { url: osmUrl },
        success: function (response) {
          // Handle the response from the server
          console.log(response);
        },
        error: function (error) {
          console.error('Error:', error);
        },
      });
    }
  }

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
