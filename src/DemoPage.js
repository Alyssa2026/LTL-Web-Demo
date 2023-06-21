import './DemoPage.css';
import { MapContainer, TileLayer } from 'react-leaflet';
import { useState } from 'react';
import { useRef, useEffect } from 'react';
import 'leaflet/dist/leaflet.css';


// Screen where the demo will be hosted
function Demo() {
  // Calling OSM API
  const [center, setCenter] = useState({lat: 41.8268, lng: -71.4025})
  const ZOOM_LEVEL = 16;
  const mapRef = useRef()
  const url =  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  // When clicked, this will get the bounds, parse and filter the location selected
  const clickMe =async ()=>{
  if (mapRef.current) {
    // Get Bounds
    const map = mapRef.current;
    const bounds = map.getBounds();
    const minLat = Number(bounds.getSouth().toFixed(2));
    const maxLat = Number(bounds.getNorth().toFixed(2));
    const minLng = Number(bounds.getWest().toFixed(2));
    const maxLng = Number(bounds.getEast().toFixed(2));

    // Call Flask server to call genProp
    const coord = {minLat, maxLat, minLng, maxLng};
   
    const response = await fetch("/genProp", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(coord)
    });
    if (response.ok) {
      console.log("response worked!");
      
    }
      
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
