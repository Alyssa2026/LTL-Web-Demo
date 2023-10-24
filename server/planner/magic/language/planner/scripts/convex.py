import numpy as np
from scipy.spatial import ConvexHull, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from shapely import geometry, ops, wkb
import random
import parse_osm_mapping
import utils


NUM_POLYS_THRESHOLD = 150 #Note: This is an upper-bound. Due to voronoi clipping, a few less polygons can be generated.

#From https://stackoverflow.com/questions/46335488
def bounding(points):
    x_coords, y_coords = zip(*points)
    return [(min(x_coords), min(y_coords)), (max(x_coords), max(y_coords))]

#From https://sgillies.net/2010/04/06/painting-punctured-polygons-with-matplotlib.html
def ring_coding(ob):
    n = len(ob.coords)
    codes = np.ones(n, dtype=Path.code_type) * Path.LINETO
    codes[0] = Path.MOVETO
    return codes

#From https://sgillies.net/2010/04/06/painting-punctured-polygons-with-matplotlib.html
def pathify(poly):
    verts = np.concatenate([np.asarray(poly.exterior)] + [np.asarray(r) for r in poly.interiors])
    codes = np.concatenate([ring_coding(poly.exterior)] + [ring_coding(r) for r in poly.interiors])
    return Path(verts, codes)

#Adapted from https://sgillies.net/2010/04/06/painting-punctured-polygons-with-matplotlib.html
def plot_poly_with_holes(polyhole, ax, boundary, facecolor, edgecolor):
    path = pathify(polyhole)
    patch = PathPatch(path, facecolor=facecolor, edgecolor=edgecolor)

    ax.add_patch(patch)
    ax.set_xlim(boundary[0][0], boundary[1][0])
    ax.set_ylim(boundary[0][1], boundary[1][1])
    ax.set_aspect(1.0)

#Adapted from https://codereview.stackexchange.com/questions/69833
def random_points_within(poly, num):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    counter = 0
    while len(points) < num:
        randpoint = geometry.Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
        if randpoint.within(poly):
            points.append(randpoint)
        if counter > num * 3:
            print("WARNING: random point generation taking long time")
        counter += 1
    return points

#Adapted from https://stackoverflow.com/questions/34968838
def descretize_voronoi_to_polys(vor, bbox):
    points = vor.points
    lines = [geometry.LineString(vor.vertices[line]) for line in vor.ridge_vertices if -1 not in line]

    result = geometry.MultiPolygon([poly.intersection(bbox) for poly in ops.polygonize(lines)])
    result = geometry.MultiPolygon([p for p in result] + [p for p in bbox.difference(ops.unary_union(result))])

    return result

def clip_voronoi_cells(cells, clip):
    clipped = []
    for cell in cells:
        for clp in clip:
            if cell.intersects(clp):
                cell = cell.difference(clp)
        if cell.type == 'Polygon':
            clipped.append(cell)
        elif cell.type == 'MultiPolygon':
            for poly in cell:
                clipped.append(poly)
    return clipped

def map_voronoi_points(cells, points):
    point_to_cell = {}
    cell_to_point = {}
    for cell in cells:
        for p in points:
            if p.within(cell):
                point_to_cell[(p.x, p.y)] = cell
                cell_to_point[cell.wkb] = p
                break

    return point_to_cell, cell_to_point

def graph_from_voronoi(points_to_cells, cell_to_point, landmarks_to_point, points_to_landmark):
    graph = {}

    points = list(points_to_cells.keys()) + list(points_to_landmark.keys())
    merged_cells = {**points_to_cells, **points_to_landmark}

    landmarks_aspoly_to_point = {value.wkb: key for key, value in points_to_landmark.items()}
    merged_points = {**cell_to_point, **landmarks_aspoly_to_point}


    for p in merged_cells.keys():
        graph[p] = []
        curr_cell = merged_cells[p]
        for c in merged_points.keys():
            if curr_cell.intersects(wkb.loads(c)):
                if isinstance(merged_points[c], tuple):
                    graph[p].append(merged_points[c])
                else:
                    graph[p].append((merged_points[c].x, merged_points[c].y))
    return merged_cells, graph

def plot_points(points):
    for p in points:
        if isinstance(p, geometry.point.Point):
            plt.plot(p.x, p.y, marker='o', markersize=1.5)
        else:
            plt.plot(p[0], p[1], marker='o', markersize=1.5)

def plot_polys(polys):
    for poly in polys:
        plt.plot(*poly.exterior.xy, linewidth=0.5)

def plot_voronoi(v, ax):
    voronoi_plot_2d(v, ax, show_points=False, show_vertices=False, line_width=0.5)
def build_graph(ways, nodes):
    ### Plot dimensions
    fig = plt.figure(num=1, figsize=(5, 3), dpi=180)
    ax = fig.add_subplot(111)

    ### Creating convex hulls from OSM way data
    hulls = []
    landmarks_to_point = {}
    points_to_landmark = {}

    for way in ways.keys():
        points = np.array(ways[way])
        if len(points) <= 2:
            print("cannot convex")
        else:
            hull = ConvexHull(points)
            hulls.append(hull)

            pt = (hull.points[hull.vertices[0]][0], hull.points[hull.vertices[0]][1])
            landmarks_to_point[way] = pt

            verticies = [hull.points[v] for v in hull.vertices]
            as_poly = geometry.Polygon(verticies)
            points_to_landmark[(pt[0], pt[1])] = as_poly
            '''
            plt.plot(points[:,0], points[:,1], 'o')
            for simplex in hull.simplices:
                plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
            '''
    ### Converting convex hulls to polygons
    hpolys = []
    hverts = []
    hpoly_navigation_points = []
    for h in hulls:
        verticies = [h.points[v] for v in h.vertices]
        hverts.extend(verticies)
        hpoly_navigation_points.append(geometry.Point(verticies[0][0], verticies[0][1]))
        hpolys.append(geometry.Polygon(verticies))
    plot_polys(hpolys)
    ### Creating polygons for landmarks
    lpolys = []
    lpoly_navigation_points = []
    for n in nodes.keys():
        centerpt = nodes[n]

        d1, d2 = utils.gdiag(utils.meters_to_miles(3), centerpt)
        points = np.array([(d1[0], d1[1]), (d2[0], d2[1]), (d1[0], d2[1]), (d2[0], d1[1])])

        bbox = ConvexHull(points)
        bbox_aspoly = geometry.Polygon([bbox.points[v] for v in bbox.vertices])
        lpolys.append(bbox_aspoly)

        pt = (bbox.points[bbox.vertices[0]][0], bbox.points[bbox.vertices[0]][1])
        lpoly_navigation_points.append(geometry.Point(pt[0], pt[1]))
        #lpoly_navigation_points.append(geometry.Point(centerpt[0], centerpt[1]))
        landmarks_to_point[n] = pt
        points_to_landmark[pt] = bbox_aspoly

    ### Merging overlapping polygons
    merged = ops.cascaded_union(hpolys + lpolys)

    ### Creating map boundary polygon
    boundary = bounding(hverts)
    bbox = geometry.box(boundary[0][0], boundary[0][1], boundary[1][0], boundary[1][1])

    ### Symmetric difference polygon, between bounding box and ways
    polyhole = geometry.Polygon(bbox.exterior.coords, [m.exterior.coords for m in merged])
    plot_poly_with_holes(polyhole, ax, boundary, facecolor='#cccccc', edgecolor='#999999')

    ### Get NUMPOLY number of points in symmetric difference polygon
    randpoints = random_points_within(polyhole, NUM_POLYS_THRESHOLD)
    #plot_points(randpoints)

    ### Get voronoi diagram of points
    vor = Voronoi(np.array([[r.x, r.y] for r in randpoints]))
    vor_p = descretize_voronoi_to_polys(vor, bbox)
    #plot_polys(vor_p)

    ### Clip voronoi cells that overlap way polys
    clipped = clip_voronoi_cells(cells=vor_p, clip=merged)
    #plot_polys(clipped)

    ### Map each point to its cell, remove extra points
    mapping_points = randpoints + hpoly_navigation_points + lpoly_navigation_points
    point_to_cell, cell_to_point = map_voronoi_points(cells=clipped + [m for m in merged], points=mapping_points)
    #plot_points(point_to_cell.keys())

    ### Build graph from cells
    merged_cells, graph = graph_from_voronoi(point_to_cell, cell_to_point, landmarks_to_point, points_to_landmark)
    #plt.show()
    return point_to_cell, cell_to_point, landmarks_to_point, merged_cells, graph

def main():
    build_graph()
    '''
    ### Plot dimensions
    fig = plt.figure(num=1, figsize=(5, 3), dpi=180)
    ax = fig.add_subplot(111)

    ### Creating convex hulls from OSM way data
    ways = parse_osm_mapping.get_ways()
    hulls = []

    for way in ways.keys():
        points = np.array(ways[way])
        if len(points) <= 2:
            print("cannot convex")
        else:
            hull = ConvexHull(points)
            hulls.append(hull)

            plt.plot(points[:,0], points[:,1], 'o')
            for simplex in hull.simplices:
                plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    ### Converting convex hulls to polygons
    hpolys = []
    hverts = []
    for h in hulls:
        verticies = [h.points[v] for v in h.vertices]
        hverts.extend(verticies)
        hpolys.append(geometry.Polygon(verticies))

    ### Merging overlapping polygons
    merged = ops.cascaded_union(hpolys)

    ### Creating map boundary polygon
    boundary = bounding(hverts)
    bbox = geometry.box(boundary[0][0], boundary[0][1], boundary[1][0], boundary[1][1])

    ### Symmetric difference polygon, between bounding box and ways
    polyhole = geometry.Polygon(bbox.exterior.coords, [m.exterior.coords for m in merged])
    plot_poly_with_holes(polyhole, ax, boundary, facecolor='#cccccc', edgecolor='#999999')

    ### Get NUMPOLY number of points in symmetric difference polygon
    randpoints = random_points_within(polyhole, NUM_POLYS_THRESHOLD)
    #plot_points(randpoints)

    ### Get voronoi diagram of points
    vor = Voronoi(np.array([[r.x, r.y] for r in randpoints]))
    vor_p = descretize_voronoi_to_polys(vor, bbox)
    #plot_polys(vor_p)

    ### Clip voronoi cells that overlap way polys
    clipped = clip_voronoi_cells(cells=vor_p, clip=merged)
    plot_polys(clipped)

    ### Map each point to its voronoi cell, remove extra points
    point_to_cell, cell_to_point = map_voronoi_points(cells=clipped, points=randpoints)
    plot_points(point_to_cell.keys())

    ### Build graph from voronoi cells
    graph = graph_from_voronoi(point_to_cell, cell_to_point)
    print(graph)
    '''
    #plt.show()


if __name__=="__main__":
    main()
