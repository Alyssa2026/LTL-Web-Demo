from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import xml.etree.ElementTree as ET
import re
from string import digits

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/genProp", methods = ['POST'] )
def genProp():
    # Get the coord to form the URL to make JSON file
    data = request.get_json()
    minLat = data['minLat']
    maxLat = data['maxLat']
    minLng = data['minLng']
    maxLng = data['maxLng']
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={minLng},{minLat},{maxLng},{maxLat}"

    # Make a request to retrieve the XML content
    response = requests.get(url)
    osm_content = response.text

    # Parse the XML content
    root = ET.fromstring(osm_content)
    # Define a dictionary to store the extracted names (set to avoid repeats)
    names = {}
    node_coordinates = {}

    # Iterate over the elements in the OSM file
    for element in root.iter():
        if element.tag == 'node':
                node_id = element.attrib.get('id')
                node_lat = float(element.attrib.get('lat'))
                node_lon = float(element.attrib.get('lon'))
                node_coordinates[node_id] = (node_lat, node_lon)
        elif element.tag == 'way':
        # Check if the element represents a building or business 
            for child in element:
                # Extract the name tag value if building exists
                if child.tag == 'tag':
                    if child.attrib.get('k') == 'building' or child.attrib.get('k') == 'amenity' or child.attrib.get('k') == 'shop':
                        val = child.attrib.get('v')
                        mapToDic = {}
                        for child in element:
                        # Check for the 'tag' elements that contain the name information
                            if child.tag == 'tag' and child.attrib.get('k') == 'name':
                                # make all characters lower case, remove any leading numbers, replace all special characters and space with '_'
                                name = re.sub(r"[!@#$%^&*()\[\]{};:,.\/<>?\|`~+=\s]", "_", (child.attrib.get('v')).lower().lstrip(digits))
                                names.setdefault(name, val)
                                # add semantic info
                            elif child.tag == 'tag':
                                        mapToDic[child.attrib.get('k').lower()]=child.attrib.get('v').lower()
                        # add name and coordinates
                        if name and mapToDic:
                            coords = []
                            for nd in element.iter("nd"):
                                ref = nd.attrib.get('ref')
                                if ref in node_coordinates:
                                    lat, lon = node_coordinates[ref]
                                    coords.append((lat, lon))
                                                            

                            # Calculate the center coordinate of the way
                            center_lat = sum(lat for lat, lon in coords) / len(coords)
                            center_lon = sum(lon for lat, lon in coords) / len(coords)

                            # Add the center coordinate to the mapToDic dictionary
                            mapToDic['latitude'] = center_lat
                            mapToDic['longitude']=center_lon
                            names[name] = mapToDic
                           
                            

                            

    # return out all the names 

    return jsonify(names)

   
if __name__ == '__main__':
    app.run(debug= True, port = 5002)
