import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
from string import digits
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/routeSeq", methods = ['POST'] )
def routeSeq():
    # Get the LTL statement, proposition JSON File, and map boundaries
    data = request.get_json()
    # coordinates
    minLat = data['minLat']
    maxLat = data['maxLat']
    minLng = data['minLng']
    maxLng = data['maxLng']
    # LTL 
    LTLStatement = data['LTLStatement']
    # JSON file
    file = data['file']
    dict = json.loads(file)

   # create environment

   # map number to location
    numToLoc= {}
    i = 0
    allLoc =[]
    env = {}
    for key in dict:
        numToLoc[i]=key
        allLoc.append(i)
        i+=1
        
    for i in range(len(dict)):
        env[i]=allLoc
    out = [numToLoc, allLoc]
    coordList = []
    # create 5 random coordiates:
    for i in range(5):
        coord = [random.uniform(minLat+0.0004, maxLat-0.0004), random.uniform(minLng+0.0004, maxLng-0.0004)]
        coordList.append(coord)

    return jsonify(coordList)
   
   
if __name__ == '__main__':
    app.run(debug= True, port = 5003)
