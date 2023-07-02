
# Lang2LTL Web Demo

Welcome! This demo showcases the capabilities of Lang2LTL, a powerful software that translates natural language commands into Linear Temporal Logic (LTL) statements. 

## Run Locally

Clone the project:

```bash
  git clone https://github.com/Alyssa2026/LTL-Web-Demo.git
```

Start backend servers 

```bash
  python server/genPropServer.py
```
```bash
  python server/LTLServer.py
```
Navigate to frontend demo

```bash
  cd client
```

Install dependencies

```bash
  npm install
```

Start frontend server

```bash
  npm start
```
## How to Use Demo

The demo starts off at a homepage. Click the "Go to Demo Page" to get directed to the demo.

Enter a natural language command in the first input box and click the "convert to LTL" button.

\\ Add more as project progresses 

## Project Outline 

### Client
Holds all the frontend components of the demo

#### Src
Holds all the relevant code that constructs the frontend demo

* App.js creates a path from the homepage to demopage
* DemoPage.js creates the demopage
    
    * clickMe takes in user's NL input, gets the OSM coordinates, and sends the coordiantes to the backend server where it is processed by the genProp() method
    * OSM API is integrated here

* HomePage.js creates homepage

### Server
Holds all the backend components of the demo 

* genPropServer.py is the first server. GenProp() method parses/filters an OSM file based on the coordinates passed in from the frontend input

* LTLServer.py is the second server. DisplayLTL() method that takes in the NL command, Go to Slater Hall then Salomon Center for Teaching, and returns the LTL expression back to the frontend, G(Slater Hall->X(Salomon Center for Teaching)). Note: Using constant inputs/outputs for now before we integrate the LTL software


        

    


