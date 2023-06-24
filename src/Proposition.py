import xml.etree.ElementTree as ET
import re
from string import digits
import requests
# Flask server imports
from flask import Blueprint, jsonify, request

main = Blueprint('main',__name__ )

@main.route('/genProp', methods = ['POST'])
def genProp():
    # Get the URL from the request JSON
    print ('hello')