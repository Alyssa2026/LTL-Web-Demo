#######################################################
#           Lat/Long Support Functions                #
#######################################################
import math
import requests


def get_lat(p):
    assert(isinstance(p, tuple)), ("%s datatype not supported as lat/long datatype" % type(p))
    return p[0]

def get_lon(p):
    assert(isinstance(p, tuple)), ("%s datatype not supported as lat/long datatype" % type(p))
    return p[1]

# Calculate great-circle distance between two points
# Credit: https://www.movable-type.co.uk/scripts/latlong.html
def haversine_distance(p1, p2):
    r = 6371e3
    print("p1", p1)
    print("p2", p2)
    del_lat = abs(math.radians(get_lat(p2) - get_lat(p1)))
    del_lon = abs(math.radians(get_lon(p2) - get_lon(p1)))

    a = math.sin(del_lat / 2) * math.sin(del_lat / 2) + math.cos(get_lat(p1)) * math.cos(get_lat(p2)) * math.sin(del_lon / 2) * math.sin(del_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c

    return d

# Returns SW, NE lat/long points x meters from p
# Credit: https://gis.stackexchange.com/questions/15545/calculating-coordinates-of-square-x-miles-from-center-point
def gdiag(r, p):
    NS = r / 69
    EW = NS / math.cos(get_lat(p))

    d1 = (get_lat(p) - NS, get_lon(p) + EW)
    d2 = (get_lat(p) + NS, get_lon(p) - EW)

    return d1, d2
#    return (round(d1[0], 6), round(d1[1], 6)), ((round(d2[0], 6)), round(d2[1], 6))

# Scrape 5m box of landmarks around drone pos
def create_map_from_osm(p, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"

    left_bound, right_bound = gdiag(meters_to_miles(radius), p)
    print("left bound:", left_bound)
    print("right bound:", right_bound)
    # Overpass query gets all named nodes and named ways that aren't too large 
    # [!] tags exclude large ways
    overpass_query = """
    [out:json];
    (node["name"]( {}, {}, {}, {});
    way["name"!="Brown University"]["name"][!"place"][!"highway"][!"railway"]({}, {}, {}, {});
    );
    (._;>;);
    out body;
    """.format(left_bound[0], left_bound[1], right_bound[0], right_bound[1], left_bound[0], left_bound[1], right_bound[0], right_bound[1])

    print("QUERY:", overpass_query)

    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data

def meters_to_miles(mt):
    return mt / 1609.344
