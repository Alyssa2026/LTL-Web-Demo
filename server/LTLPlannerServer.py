import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
from string import digits
from flask_cors import CORS, cross_origin
import random
from collections import defaultdict
import build_graph_env
#from magic.language.planner.scripts.simple_rl.simple_rl.apmdp.settings import build_graph_env


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
    cube_env = build_graph_env.build_graph_env(dict)

    coordList = []
    return jsonify(cube_env)
    # create 5 random coordiates:
    for i in range(5):
        coord = [random.uniform(minLat+0.0004, maxLat-0.0004), random.uniform(minLng+0.0004, maxLng-0.0004)]
        coordList.append(coord)

    return jsonify(coordList)
   
   
if __name__ == '__main__':
    app.run(debug= True, port = 5008)
