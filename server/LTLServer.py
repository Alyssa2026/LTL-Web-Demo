from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
from string import digits
from flask_cors import CORS, cross_origin
from lang2ltl import lang2ltl


app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/convertLTL", methods = ['POST'] )
def convertLTL():
   # Get the user input and proposition JSON File
   data = request.get_json()
   user_input = data.get('input')
   file = data.get('file')
   # Read the first line of the JSON file
   # first_line = ''
   # with open(file, 'r') as json_file:
   #first_line = json_file.readline()impo
  

   try:
        result =lang2ltl(user_input, file, 3) # random last input until keepKeys is figured out
        return jsonify(result)
   except Exception as e:
        error_message = "An error occurred while processing the request."
        print(error_message, e)  # Print the error message and the exception
        return jsonify({"error": str(e)}), 500  # Return an appropriate error response

   

   # return the user input 
   # return jsonify(user_input)
   # return the file 
   # return jsonify(file)

   return jsonify('G(Slater Hall -> X(Salomon Center For Teaching))')
   
   
if __name__ == '__main__':
    app.run(debug= True, port = 5002)
