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

    # Iterate over the elements in the OSM file
    for element in root.iter():
        # Check if the element represents a building or business 
        if element.tag == 'way' or element == 'node':
            for child in element:
                # Extract the name tag value if building exists
                if child.tag == 'tag':
                    if child.attrib.get('k') == 'building' or child.attrib.get('k') == 'amenity' or child.attrib.get('k') == 'shop':
                        val = child.attrib.get('v')
                        for child in element:
                        # Check for the 'tag' elements that contain the name information
                            if child.tag == 'tag' and child.attrib.get('k') == 'name':
                                # make all characters lower case, remove any leading numbers, replace all special characters and space with '_'
                                name = re.sub(r"[!@#$%^&*()\[\]{};:,.\/<>?\|`~+=\s]", "_", (child.attrib.get('v')).lower().lstrip(digits))
                                names.setdefault(name, val)
                                # add designation
                                for child in element:
                                    if child.tag == 'tag' and child.attrib.get('k') == 'designation':
                                        names[name] = child.attrib.get('v').lower()

    # return out all the names 

    return jsonify(names)

   
if __name__ == '__main__':
    app.run(debug= True, port = 5001)
