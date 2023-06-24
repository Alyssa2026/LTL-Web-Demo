import './DemoPage.css';
import { MapContainer, TileLayer } from 'react-leaflet';
import { useRef, useState} from 'react';
import 'leaflet/dist/leaflet.css';
import axios from 'axios'

// Screen where the demo will be hosted
function Demo() {
  // Calling OSM API
  const [center, setCenter] = useState({lat: 41.8268, lng: -71.4025})
  const ZOOM_LEVEL = 16;
  const mapRef = useRef()
  const url =  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  
  // When clicked, this will collect the user inpits, get the bounds, parse and filter the location selected
  const [response, setResponse] = useState(''); // JSON File
  let userInputValue; // Declare the variable outside the function

  const clickMe =async ()=>{

  // Get use input
  userInputValue = document.getElementById("textInput").value;
  // Do something with the userInput value
  console.log("User input: " + userInputValue);

  if (mapRef.current) {
      // Get Bounds
      const map = mapRef.current;
      const bounds = map.getBounds();
      const minLat = Number(bounds.getSouth().toFixed(2));
      const maxLat = Number(bounds.getNorth().toFixed(2));
      const minLng = Number(bounds.getWest().toFixed(2));
      const maxLng = Number(bounds.getEast().toFixed(2));

      const coord = {minLat, maxLat, minLng, maxLng};
      // Call Flask server to call genProp
      try {
        const response = await axios.post('http://localhost:5001/genProp', coord);
        const responseData = response.data;
        setResponse(responseData); 
        console.log(response)

      } catch (error) {
        console.error('Error:', error);
      
      };
  }
}

// Implementing API/Logos
  return (
    <div className="backround-color" >
      <h1 style={{ fontSize: 20, marginLeft: '2in', marginTop: '1in'  }}>
        Enter Natural Language Command:
      </h1>
     
      <h2 style={{ fontSize: 20, marginLeft: '2in' }}>
        <input type= "text" id="textInput"></input>
        <button onClick={clickMe}>
          Convert to LTL
        </button>
      </h2>

      <h3 style={{ fontSize: 20, marginLeft: '2in'}}>
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
