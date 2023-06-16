import xml.etree.ElementTree as ET
import re
from string import digits
import requests

# Load the OSM file--> initial method of already downloaded file
# tree = ET.parse('PropositionGen/prov.osm')
# root = tree.getroot()

# Parse file using link directly--> potentially easier for when implementing web demo
url = 'https://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145'
response = requests.get(url)
osm_content = response.text
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
                            name = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=+]", "_", (child.attrib.get('v')).lower().lstrip(digits))
                            names.setdefault(name, val)
                            # add designation
                            for child in element:
                                if child.tag == 'tag' and child.attrib.get('k') == 'designation':
                                     names[name] = child.attrib.get('v')

# Print out all the names 
print(names)
