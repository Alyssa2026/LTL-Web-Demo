import './DemoPage.css';
import { MapContainer, TileLayer , Marker, Polyline} from 'react-leaflet';
import  L from 'leaflet';
import { useEffect, useRef, useState} from 'react';
import 'leaflet/dist/leaflet.css';
import axios from 'axios'
import end from'./img/end.png' ;
import middle from './img/middle.png' ;
import start from './img/start.png' ;

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
  const [buttonClicked, setButtonClicked] = useState(false);
  const [LTLPlannerServerResponse, setLTLPlannerServerResponse] = useState('');
  const [coordList, setCoordList] = useState([]);
  const [showMarkers, setShowMarkers] = useState(false);

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
  if (mapRef.current) {
      // Get user input
      const input = document.getElementById("textInput").value;

      // Move setUserInputValue here
      setUserInputValue(input);
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
        const response = await axios.post('http://localhost:5002/genProp', coord);
        const responseData = response.data;
        setResponse(responseData); 

         // Use the JSON file obtained in the first API call
        const jsonFile = JSON.stringify(responseData);
        console.log(responseData)
        // LTLServer to call convertLTL(), passes in user input and JSON file of Propositions
        const response2 = await axios.post('http://localhost:5004/convertLTL',  { input: userInputValue, file: jsonFile});
        const responseData2 = response2.data;
        setLTLServerResponse(responseData2);
        console.log(responseData2);
        // LTLPlannerServer called to get route sequence 
        const response3 = await axios.post('http://localhost:5008/routeSeq',  {LTLStatement: responseData2, file: jsonFile, minLat: 
        minLat, maxLat: maxLat, minLng:minLng, maxLng: maxLng});
        const responseData3 = response3.data;
        setLTLPlannerServerResponse(responseData3);
        setCoordList(responseData3);
        console.log(responseData3);
        setShowMarkers(true);

      } catch (error) {
        if (error.config.url === 'http://localhost:5002/convertLTL') {
          console.log("Error from convertLTL:", error.response.data.error); // Log the error message
        }
        console.error('Error:', error);
      
      };
      setButtonClicked(true)
  }
}

// Creating custom marker for Map
const startMark = L.icon({
  iconUrl: start,
  iconSize: [32, 32], // Adjust the size of the icon as needed
  iconAnchor: [16, 32],
});

const endMark =
L.icon({
  iconUrl: end,
  iconSize: [32, 32], // Adjust the size of the icon as needed
  iconAnchor: [16, 32],
});

const middleMark =
L.icon({
  iconUrl: middle,
  iconSize: [32, 32], // Adjust the size of the icon as needed
  iconAnchor: [16, 32],
});


// Implementing OSM API and creating demo page components 
  return (
    <div className="backround-color" >
      <h1 style={{ fontSize: 20, marginLeft: '2in', marginTop: '1in'  }}>
        Enter Natural Language Command:
      </h1>
     
      <h2 style={{ fontSize: 20, marginLeft: '2in' }}>
          <input
            type="text"
            id="textInput"
            value={userInputValue}
            onChange={(e) => setUserInputValue(e.target.value)}
          />
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
           {showMarkers && coordList.length > 0 && (
            <>
              <Marker position={coordList[0]} icon={startMark} />
              <Marker
                position={coordList[coordList.length - 1]}
                icon={endMark}
              />
              {coordList.map((coord, index) =>
               index !== 0 && index !== coordList.length - 2 ? (
                 <Marker key={index} position={coord} icon={middleMark} />
               ) : null
              )}
             <Polyline positions={coordList} color="black" />

            </>
          )}
        </MapContainer>
      </div>
   </div>  
  );
}

export default Demo;
