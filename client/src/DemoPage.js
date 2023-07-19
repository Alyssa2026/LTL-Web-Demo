import './DemoPage.css';
import { MapContainer, TileLayer , Marker} from 'react-leaflet';
import { useEffect, useRef, useState} from 'react';
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
  const [userInputValue, setUserInputValue] = useState(''); // set up constant for user input
  const [ltlServerResponse, setLTLServerResponse] = useState('');

  // usereffect to update local storage
  useEffect(() => {
    const storedOut = JSON.parse(localStorage.getItem('server output')) || [];
    storedOut.push(ltlServerResponse);
    localStorage.setItem('server output', JSON.stringify(storedOut));

    const storedIn = JSON.parse(localStorage.getItem('user input')) || [];
    storedIn.push(userInputValue);
    localStorage.setItem('user input', JSON.stringify(storedIn));
  }, [userInputValue, ltlServerResponse]);
  
  const clickMe =async ()=>{
  // Get user input
  const input = document.getElementById("textInput").value;
  setUserInputValue(input);
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
      // Call servers required when button is clicked
      try {
         // Call genProp server to call genProp()
        const response = await axios.post('http://localhost:5001/genProp', coord);
        const responseData = response.data;
        setResponse(responseData); 

         // Use the JSON file obtained in the first API call
        const jsonFile = JSON.stringify(responseData);
        console.log(responseData)
        // LTLServer to call convertLTL(), passes in user input and JSON file of Propositions
        const response2 = await axios.post('http://localhost:5002/convertLTL',  { input: userInputValue, file: jsonFile});
        const responseData2 = response2.data;
        setLTLServerResponse(responseData2);
        console.log(responseData2);
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
            <Marker position={[41.826409, -71.402863]} />
            <Marker position={[41.8258, -71.40427]} />
        </MapContainer>
      </div>
   </div>  
  );
}

export default Demo;
