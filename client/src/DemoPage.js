import './DemoPage.css';
import { MapContainer, TileLayer } from 'react-leaflet';
import { useRef, useState} from 'react';
import 'leaflet/dist/leaflet.css';
import axios from 'axios'

// Screen where the demo will be hosted
function Demo() {
  // Getting the OSM API
  const [center, setCenter] = useState({lat: 41.8268, lng: -71.4025})
  const ZOOM_LEVEL = 16;
  const mapRef = useRef()
  const url =  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  
  // When button is clicked, this will collect the user inputs, get the bounds, parse and filter the location selected
  const [response, setResponse] = useState(''); // Record genProp output 
  let userInputValue; // Declare the variable outside the function
  const [ltlServerResponse, setLTLServerResponse] = useState('');
  const clickMe =async ()=>{

  // Get user input
  userInputValue = document.getElementById("textInput").value;

  if (mapRef.current) {
      // Get bounds of area displayed on the OSM map
      const map = mapRef.current;
      const bounds = map.getBounds();
      const minLat = Number(bounds.getSouth());
      const maxLat = Number(bounds.getNorth());
      const minLng = Number(bounds.getWest());
      const maxLng = Number(bounds.getEast());

      const coord = {minLat, maxLat, minLng, maxLng};
      console.log(coord)
      // Call genProp server to call genProp()
      try {
        const response = await axios.post('http://localhost:5001/genProp', coord);
        const responseData = response.data;
        setResponse(responseData); 
        console.log(response)

      } catch (error) {
        console.error('Error:', error);
      
      };
      // LTLServer to call displayLTL()
      try {
        const response = await axios.post('http://localhost:5002/displayLTL',  { input: userInputValue });
        const responseData = response.data;
        setLTLServerResponse(responseData);
        console.log(responseData);
      } catch (error) {
        console.error('Error:', error);
      };
  }
}

// Implementing OSM API and creating demo page components 
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
         LTL Output:
      </h4>
      <h2 style={{ fontSize: 20, marginLeft: '2in' }}>
        {ltlServerResponse}
      </h2>
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
